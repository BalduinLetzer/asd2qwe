# coding: utf-8

"""
Configuration of the HH -> bbWW analysis.
"""

import os

import law
import order as od


thisdir = os.path.dirname(os.path.abspath(__file__))

#
# the main analysis object
#

analysis_asd = od.Analysis(
    name="analysis_asd",
    id=1,
)

# analysis-global versions
analysis_asd.set_aux("versions", {
})

# files of sandboxes that might be required by remote tasks
# (used in cf.HTCondorWorkflow)
analysis_asd.x.bash_sandboxes = [
    "$CF_BASE/sandboxes/cf_prod.sh",
    "$CF_BASE/sandboxes/venv_columnar.sh",
    # "$ASD_BASE/sandboxes/venv_columnar_tf.sh",
]

# cmssw sandboxes that should be bundled for remote jobs in case they are needed
analysis_asd.set_aux("cmssw_sandboxes", [
    # "$CF_BASE/sandboxes/cmssw_default.sh",
])


# clear the list when cmssw bundling is disabled
if not law.util.flag_to_bool(os.getenv("ASD_BUNDLE_CMSSW", "1")):
    del analysis_asd.x.cmssw_sandboxes[:]

# config groups for conveniently looping over certain configs
# (used in wrapper_factory)
analysis_asd.set_aux("config_groups", {})

# trailing imports for different configs
import asd.config.config_2017  # noqa
# import asd.config.config_2018  # noqa
