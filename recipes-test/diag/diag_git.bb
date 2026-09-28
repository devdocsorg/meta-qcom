SUMMARY = "DIAG implements routing of diagnostics related messages between host and various subsystems."
HOMEPAGE = "https://github.com/linux-msm/diag"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=f6832ae4af693c6f31ffd931e25ef580"

SRC_URI = "git://github.com/linux-msm/${BPN}.git;branch=master;protocol=https"

PV = "0.0+git"
SRCREV = "d06e599d197790c9e84ac41a51bf124a69768c4f"

DEPENDS = "qrtr udev"
RPROVIDES:${PN} = "virtual-diag-router"
RCONFLICTS:${PN} = "diag-router"

# @description Build diag with the upstream Makefile.
# @noargs
# @exitcode 0 The binaries are built.
# @exitcode >0 The build failed; BitBake stops the task.
# @example
#   bitbake -c compile diag
do_compile () {
	oe_runmake
}

# @description Install diag with the upstream Makefile `install` target.
# @noargs
# @exitcode 0 The binaries are in the install directory.
# @exitcode >0 The make install step failed; BitBake stops the task.
# @example
#   bitbake -c install diag
do_install () {
	oe_runmake install 'DESTDIR=${D}'
}
