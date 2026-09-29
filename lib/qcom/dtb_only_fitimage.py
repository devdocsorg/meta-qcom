# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#
# This file contains functions for Qualcomm-specific DTB-only FIT image generation,
# which imports classes from OE-Core fitimage.py and enhances to meet Qualcomm FIT
# specifications.
#
# For details on Qualcomm DTB metadata and FIT requirements, see:
# https://github.com/qualcomm-linux/qcom-dtb-metadata/blob/main/Documentation.md

import os
import shlex
import subprocess
import bb
from typing import Tuple, List, Dict
from oe.fitimage import ItsNodeRootKernel, ItsNodeConfiguration

# Custom extension of ItsNodeRootKernel to inject compatible strings
class QcomItsNodeRoot(ItsNodeRootKernel):

    def __init__(self, description, address_cells, conf_prefix, mkimage=None):
        """Set up an empty DTB-only FIT image tree for the arm64 architecture.

        Args:
            description (str): Value of the root ``description`` property (``FIT_DESC``).
            address_cells (str): Value of the root ``#address-cells`` property
                (``FIT_ADDRESS_CELLS``).
            conf_prefix (str): Prefix of the configuration node names, such as ``conf-``
                (``FIT_CONF_PREFIX``).
            mkimage (str, optional): Path of the ``mkimage`` binary that
                ``run_mkimage_assemble`` runs. Defaults to None.

        Example:
            ``do_generate_qcom_fitimage`` calls ``QcomItsNodeRoot(d.getVar("FIT_DESC"),
            d.getVar("FIT_ADDRESS_CELLS"), d.getVar("FIT_CONF_PREFIX"), d.getVar("MKIMAGE"))``.
        """
        # We only pass the essential parameters needed for QCOM DTB-only FIT image generation
        # because FIT features like signing, hashing, and padding are not required here.
        # The fit_os value is unused since no kernel node is emitted.
        super().__init__(description, address_cells, None, "arm64", None, conf_prefix,
                         mkimage=mkimage)

        self._mkimage_extra_opts = []
        self._dtbs = []

    def set_extra_opts(self, mkimage_extra_opts):
        """Store extra ``mkimage`` options to use when the FIT image is assembled.

        Args:
            mkimage_extra_opts (str): Options as one shell-quoted string, such as the value
                of ``FIT_DTB_MKIMAGE_EXTRA_OPTS``; an empty string or None clears them.

        Example:
            ``root_node.set_extra_opts("-E -B 8")`` makes ``run_mkimage_assemble`` run
            ``mkimage -E -B 8 -f <itsfile> <fitfile>``.
        """
        self._mkimage_extra_opts = shlex.split(mkimage_extra_opts) if mkimage_extra_opts else []

    # Emit the DTB section for the FIT image
    def fitimage_emit_section_dtb(self, dtb_id, dtb_path,
                                  compatible_str=None,
                                  dtb_type=None):
        """Add an ``fdt-<dtb_id>`` image node and record it for the configuration sections.

        Unlike the OE-Core method it overrides, this sets no load address and records the
        compatible strings given by the caller instead of reading them from the file.

        Args:
            dtb_id (str): Image identifier, normally the file name with commas replaced by
                underscores, such as ``qcs6490-rb3gen2.dtb``.
            dtb_path (str): Path of the file that the node includes with ``/incbin/``.
            compatible_str (str, optional): Space-separated compatible strings of the
                configurations that boot this DTB on its own; None or "" for none.
            dtb_type (str, optional): Value of the node's ``type`` property, such as
                ``flat_dt`` or ``qcom_metadata``.

        Example:
            ``root_node.fitimage_emit_section_dtb("qcom-metadata.dtb", qcom_meta,
            compatible_str=None, dtb_type="qcom_metadata")`` adds the
            ``fdt-qcom-metadata.dtb`` image node.
        """
        load = None
        dtb_ext = os.path.splitext(dtb_path)[1]

        opt_props = {
            "data": '/incbin/("' + dtb_path + '")',
            "arch": self._arch
        }
        if load:
            opt_props["load"] = f"<{load}>"

        dtb_node = self.its_add_node_dtb(
            "fdt-" + dtb_id,
            "Flattened Device Tree blob",
            dtb_type,
            "none",
            opt_props,
            compatible_str
        )
        self._dtbs.append((dtb_node, compatible_str or "", dtb_id))

    def _fitimage_emit_one_section_config(self, conf_node_name, dtb=None):
        """Emit the fitImage ITS configuration section

        Adds one node under ``configurations`` with the description "FDT Blob". When a DTB
        node is given, the configuration's ``fdt`` is that node's name and its
        ``compatible`` is the node's current ``compatible`` attribute, if set.

        Args:
            conf_node_name (str): Name of the configuration node, such as ``conf-1``.
            dtb (oe.fitimage.ItsNodeDtb, optional): Image node that the configuration
                boots; None emits a configuration with only a description.

        Example:
            With ``dtb_node.compatible = "qcom,board-iot"``,
            ``self._fitimage_emit_one_section_config("conf-1", dtb_node)`` adds
            ``conf-1`` with ``fdt = "fdt-board.dtb"`` and ``compatible = "qcom,board-iot"``.
        """
        opt_props = {}
        conf_desc = []

        if dtb:
            conf_desc.append("FDT blob")
            opt_props["fdt"] = dtb.name
            if dtb.compatible:
                opt_props["compatible"] = dtb.compatible

        ItsNodeConfiguration(
            conf_node_name,
            self.configurations,
            description="FDT Blob",
            opt_props=opt_props
        )

    def fitimage_emit_section_config(self):
        """Add one configuration per compatible string of each recorded non-metadata DTB.

        Configurations are numbered ``<conf_prefix>1``, ``<conf_prefix>2`` and so on.
        Overlay combinations are not handled; ``do_generate_qcom_fitimage`` calls
        ``fitimage_emit_section_qcomconfig`` instead of this method.

        Raises:
            ValueError: When any DTB has been recorded, because the loop unpacks two values
                from the three-item ``(node, compatible_str, dtb_id)`` entries that
                ``fitimage_emit_section_dtb`` stores.

        Example:
            ``root_node.fitimage_emit_section_config()``, called after the DTB sections
            have been emitted.
        """
        counter = 0
        for dtb_node, compatible_str in self._dtbs:
            # qcom-metadata don't need any config entry
            if dtb_node.properties.get("type") == "qcom_metadata":
                continue
            # add one config for each compatible string of DTB
            for compatible in compatible_str.split():
                counter += 1
                conf_name = f"{self._conf_prefix}{counter}"
                dtb_node.compatible = compatible
                self._fitimage_emit_one_section_config(conf_name, dtb_node)

    def fitimage_emit_section_qcomconfig(self, overlay_groups, overlay_compats):
        """Add the configurations for base DTBs and their overlay combinations.

        Only recorded ``.dtb`` images get configurations; the metadata blob and overlays
        are skipped. For each base DTB, one configuration is added per compatible string
        recorded with it, with ``fdt`` naming the base DTB, then one per compatible string
        of each of its overlay groups, with ``fdt`` listing the base DTB followed by the
        overlays. Configurations are numbered from ``<conf_prefix>1`` in that order, and
        each overlay lookup key is logged with ``bb.note``.

        Args:
            overlay_groups (dict[str, list[list[str]]]): Maps a base DTB id, such as
                ``board.dtb``, to its overlay lists, such as ``[["camx.dtbo"]]``; None
                means no overlays.
            overlay_compats (dict[str, str]): Maps the space-joined stems of a base DTB and
                its overlays, with commas replaced by underscores (such as ``board camx``),
                to their space-separated compatible strings; None means none.

        Example:
            ``root_node.fitimage_emit_section_qcomconfig({"board.dtb": [["camx.dtbo"]]},
            {"board camx": "qcom,board-iot-subtype2"})`` adds the base configurations of
            ``board.dtb``, then one for ``qcom,board-iot-subtype2`` with
            ``fdt = "fdt-board.dtb", "fdt-camx.dtbo"``.
        """
        counter = 1
        for (dtb_node, compatible_str, dtb_id) in self._dtbs:
            # qcom-metadata doesn't need any config entry
            if dtb_node.properties.get("type") == "qcom_metadata":
                continue

            # Only create config entries for base dtbs
            if not dtb_id.endswith(".dtb"):
                continue

            # Base-only configs
            base_compats = str(compatible_str or "").split()
            for compatible in base_compats:
                conf_name = f"{self._conf_prefix}{counter}"
                dtb_node.compatible = compatible
                self._fitimage_emit_one_section_config(conf_name, dtb_node)
                counter += 1

            # Overlay configs
            for ovl_list in (overlay_groups or {}).get(dtb_id, []):
                dt_list = [dtb_id] + ovl_list

                fdtentries = [f"fdt-{dt}" for dt in dt_list]
                lookup_key = " ".join([os.path.splitext(dt)[0].replace(',', '_') for dt in dt_list])
                bb.note(lookup_key)

                ovl_compats = str(((overlay_compats or {}).get(lookup_key, "")) or "").split()
                for compat in ovl_compats:
                    conf_name = f"{self._conf_prefix}{counter}"
                    dtb_node.compatible = compat
                    self._fitimage_emit_one_section_config(conf_name, dtb_node)

                    conf_node = self.configurations.sub_nodes[-1]
                    conf_node.add_property('fdt', fdtentries)
                    counter += 1

    # Override mkimage assemble to inject extra opts
    def run_mkimage_assemble(self, itsfile, fitfile):
        """Compile the ITS file into a FIT image with ``mkimage`` and the stored extra options.

        Runs ``mkimage <extra options> -f <itsfile> <fitfile>`` and logs the command with
        ``bb.note``. The inherited ``-D`` dtc option branch never applies, because the
        constructor sets no dtc options.

        Args:
            itsfile (str): Path of the ITS source written by ``write_its_file``.
            fitfile (str): Path of the FIT image to create.

        Raises:
            bb.BBHandledException: Through ``bb.fatal``, with the command, return code,
                output, and ITS path, when ``mkimage`` fails.

        Example:
            ``do_generate_qcom_fitimage`` calls ``root_node.run_mkimage_assemble(itsfile,
            fitname)`` to create ``qclinuxfitImage`` in ``${QCOMFIT_DEPLOYDIR}``.
        """
        cmd = [self._mkimage, *self._mkimage_extra_opts, '-f', itsfile, fitfile]
        if self._mkimage_dtcopts:
            cmd.insert(1, '-D')
            cmd.insert(2, self._mkimage_dtcopts)

        bb.note(f"Running mkimage with extra opts: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            bb.fatal(
                f"Command '{' '.join(cmd)}' failed with return code {e.returncode}\n"
                f"stdout: {e.stdout.decode()}\n"
                f"stderr: {e.stderr.decode()}\n"
                f"itsfile: {os.path.abspath(itsfile)}"
            )
