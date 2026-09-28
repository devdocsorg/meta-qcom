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

    # Create a DTB-only FIT root node for the arm64 architecture.
    #
    # Args:
    #     description (str): FIT image description.
    #     address_cells (str): Value for the root ``#address-cells`` property.
    #     conf_prefix (str): Prefix for configuration node names.
    #     mkimage (str): mkimage command, or None to use the base default.
    #
    # Example:
    #     ``QcomItsNodeRoot("Qualcomm FIT", "1", "conf-", "mkimage")``
    def __init__(self, description, address_cells, conf_prefix, mkimage=None):
        # We only pass the essential parameters needed for QCOM DTB-only FIT image generation
        # because FIT features like signing, hashing, and padding are not required here.
        # The fit_os value is unused since no kernel node is emitted.
        super().__init__(description, address_cells, None, "arm64", None, conf_prefix,
                         mkimage=mkimage)

        self._mkimage_extra_opts = []
        self._dtbs = []

    # Store extra mkimage options for run_mkimage_assemble.
    #
    # Args:
    #     mkimage_extra_opts (str): Shell-quoted options, or an empty value.
    #
    # Returns:
    #     None: The options are split into a list on the instance.
    #
    # Example:
    #     ``root.set_extra_opts('-E -B 8')``
    def set_extra_opts(self, mkimage_extra_opts):
        self._mkimage_extra_opts = shlex.split(mkimage_extra_opts) if mkimage_extra_opts else []

    # Emit the DTB section for the FIT image
    #
    # Adds an ``fdt-<dtb_id>`` image node and remembers it for the
    # configuration sections.
    #
    # Args:
    #     dtb_id (str): Device tree identifier, such as ``qcs6490-rb3gen2.dtb``.
    #     dtb_path (str): Path of the compiled device tree to include.
    #     compatible_str (str): Space-separated compatible strings, or None.
    #     dtb_type (str): FIT image type, such as ``flat_dt`` or ``qcom_metadata``.
    #
    # Returns:
    #     None: The node is added to the image tree.
    #
    # Example:
    #     ``root.fitimage_emit_section_dtb("qcs6490-rb3gen2.dtb", path, "qcom,qcs6490-rb3gen2", "flat_dt")``
    def fitimage_emit_section_dtb(self, dtb_id, dtb_path,
                                  compatible_str=None,
                                  dtb_type=None):
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

    # Args:
    #     conf_node_name (str): Name of the configuration node to add.
    #     dtb (oe.fitimage.ItsNode): DTB image node to reference, or None.
    #
    # Returns:
    #     None: The node is added under ``configurations``.
    #
    # Example:
    #     ``root._fitimage_emit_one_section_config("conf-1", dtb_node)``
    def _fitimage_emit_one_section_config(self, conf_node_name, dtb=None):
        """Emit the fitImage ITS configuration section"""
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

    # Add one configuration per compatible string of each stored device tree.
    #
    # Returns:
    #     None: Configuration nodes are added under ``configurations``.
    #
    # Raises:
    #     ValueError: Stored DTB entries have three items; dtb-fit-image.bbclass uses fitimage_emit_section_qcomconfig.
    #
    # Example:
    #     ``root.fitimage_emit_section_config()``
    def fitimage_emit_section_config(self):
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

    # Add configurations for each base device tree and its overlay combinations.
    #
    # Args:
    #     overlay_groups (dict): Base DTB identifier to lists of overlay
    #         identifiers applied on top of it.
    #     overlay_compats (dict): Space-joined DT names, without extensions, to
    #         the compatible strings of that combination.
    #
    # Returns:
    #     None: Configuration nodes are added; overlay ones list every fdt.
    #
    # Example:
    #     ``root.fitimage_emit_section_qcomconfig({"a.dtb": [["b.dtbo"]]}, {"a b": "qcom,a-b"})``
    def fitimage_emit_section_qcomconfig(self, overlay_groups, overlay_compats):
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
    #
    # Args:
    #     itsfile (str): Image tree source to compile.
    #     fitfile (str): FIT image to write.
    #
    # Returns:
    #     None: The FIT image is written to ``fitfile``.
    #
    # Raises:
    #     bb.BBHandledException: Through ``bb.fatal`` when mkimage fails.
    #
    # Example:
    #     ``root.run_mkimage_assemble("qcom-fit.its", "qclinuxfitImage")``
    def run_mkimage_assemble(self, itsfile, fitfile):
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
