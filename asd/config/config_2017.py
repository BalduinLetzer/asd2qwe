# coding: utf-8

"""
Configuration of the asd2qwe analysis.
"""

import os

from scinum import Number, REL
import cmsdb
import cmsdb.campaigns.run2_2017_nano_v9

from columnflow.util import DotDict, get_root_processes_from_campaign
from asd.config.categories import add_categories
from asd.config.variables import add_variables
from asd.config.jec import add_jec_files
from asd.config.external import add_external_files
from asd.config.shifts import add_shift_config
from asd.config.analysis_asd import analysis_asd

thisdir = os.path.dirname(os.path.abspath(__file__))

#
# 2017 standard config
#

# copy the campaign, which in turn copies datasets and processes
campaign_run2_2017 = cmsdb.campaigns.run2_2017_nano_v9.campaign_run2_2017_nano_v9.copy()

# get all root processes
procs = get_root_processes_from_campaign(campaign_run2_2017)

# create a config by passing the campaign, so id and name will be identical
config_2017 = analysis_asd.add_config(campaign_run2_2017)

# add processes we are interested in
config_2017.add_process(procs.n.data)
config_2017.add_process(procs.n.tt)
config_2017.add_process(procs.n.st)

# set color of some processes
colors = {
    "data": "#000000",  # black
    "tt": "#e41a1c",  # red
    "st": "#ff7f00",  # orange
    "other": "#999999",  # grey
}
for proc, color in colors.items():
    if proc in config_2017.processes:
        config_2017.get_process(proc).color1 = color

# add datasets we need to study
dataset_names = [
    # DATA
    # "data_e_b",
    # "data_e_c",
    # "data_e_d",
    # "data_e_e",
    # "data_e_f",
    # "data_mu_b",
    # "data_mu_c",
    # "data_mu_d",
    # "data_mu_e",
    # "data_mu_f",
    # TTbar
    "tt_sl_powheg",  # only one available rn
    # "tt_dl_powheg",
    # "tt_fh_powheg",
    # SingleTop
    # "st_tchannel_t_powheg",
    # "st_tchannel_tbar_powheg",
    # "st_twchannel_t_powheg",
    # "st_twchannel_tbar_powheg",
    # "st_schannel_lep_amcatnlo",
    # "st_schannel_had_amcatnlo",
]
for dataset_name in dataset_names:
    dataset = config_2017.add_dataset(campaign_run2_2017.get_dataset(dataset_name))

    # reduce n_files to max. 2 for testing purposes (TODO switch to full dataset)
    for k in dataset.info.keys():
        # if dataset.name == "ggHH_kl_1_kt_1_sl_hbbhww_powheg":
        #    continue
        if dataset[k].n_files > 2:
            dataset[k].n_files = 2

    # add aux info to datasets
    if dataset.name.startswith(("st", "tt")):
        dataset.x.has_top = True
    if dataset.name.startswith("tt"):
        dataset.x.is_ttbar = True

# default calibrator, selector, producer, ml model and inference model
config_2017.set_aux("default_calibrator", "default")
config_2017.set_aux("default_selector", "default")
config_2017.set_aux("default_producer", "features")
config_2017.set_aux("default_ml_model", None)
config_2017.set_aux("default_inference_model", "default")
config_2017.set_aux("default_categories", ["incl"])

# process groups for conveniently looping over certain processs
# (used in wrapper_factory and during plotting)
config_2017.set_aux("process_groups", {
    "default": ["st", "tt"],
})

# dataset groups for conveniently looping over certain datasets
# (used in wrapper_factory and during plotting)
config_2017.set_aux("dataset_groups", {
    "default": ["tt_*", "st_*"],
})

# category groups for conveniently looping over certain categories
# (used during plotting)
config_2017.set_aux("category_groups", {
    "default": ["incl", "1e", "1mu"],
})

# variable groups for conveniently looping over certain variables
# (used during plotting)
config_2017.set_aux("variable_groups", {
    "default": ["n_jet", "n_muon", "n_electron", "ht", "jet1_pt"],  # n_deepjet, ....
    "cutflow": ["cf_jet1_pt", "cf_jet4_pt", "cf_n_jet", "cf_n_electron", "cf_n_muon"],  # cf_n_deepjet
})

# shift groups for conveniently looping over certain shifts
# (used during plotting)
config_2017.set_aux("shift_groups", {
    "jer": ["nominal", "jer_up", "jer_down"],
})

# selector step groups for conveniently looping over certain steps
# (used in cutflow tasks)
config_2017.set_aux("selector_step_groups", {
    "default": ["Lepton", "Jet", "Bjet", "Trigger"],
})

config_2017.set_aux("selector_step_labels", {
    "Jet": r"$N_{Jets} \geq 3$",
    "Lepton": r"$N_{Lepton} = 1$",
    "Bjet": r"$N_{Jets}^{BTag} \geq 1$",
})


# 2017 luminosity with values in inverse pb and uncertainties taken from
# https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM?rev=176#LumiComb
config_2017.set_aux("luminosity", Number(41480, {
    "lumi_13TeV_2017": (REL, 0.02),
    "lumi_13TeV_1718": (REL, 0.006),
    "lumi_13TeV_correlated": (REL, 0.009),
}))

# 2017 minimum bias cross section in mb (milli) for creating PU weights, values from
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJSONFileforData?rev=44#Pileup_JSON_Files_For_Run_II
config_2017.set_aux("minbiasxs", Number(69.2, (REL, 0.046)))

# 2017 b-tag working points
# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17?rev=15
config_2017.x.btag_working_points = DotDict.wrap({
    "deepjet": {
        "loose": 0.0532,
        "medium": 0.3040,
        "tight": 0.7476,
    },
    "deepcsv": {
        "loose": 0.1355,
        "medium": 0.4506,
        "tight": 0.7738,
    },
})

# jec files
add_jec_files(config_2017)

# shift config
add_shift_config(config_2017)

# external files
add_external_files(config_2017)

# columns to keep after certain steps
config_2017.set_aux("keep_columns", DotDict.wrap({
    "cf.SelectEvents": {"mc_weight"},
    "cf.ReduceEvents": {
        # general event information
        "run", "luminosityBlock", "event",
        # weights
        "LHEWeight.*",
        "LHEPdfWeight", "LHEScaleWeight",
        # object properties
        "nJet", "Jet.pt", "Jet.eta", "Jet.phi", "Jet.mass", "Jet.btagDeepFlavB",
        "Bjet.pt", "Bjet.eta", "Bjet.phi", "Bjet.mass", "Bjet.btagDeepFlavB",
        # "Muon.*", "Electron.*", "MET.*",
        "Muon.pt", "Muon.eta", "Muon.phi", "Muon.mass",
        "Electron.pt", "Electron.eta", "Electron.phi", "Electron.mass",
        "MET.pt", "MET.phi",
        # columns added during selection, required in general
        "mc_weight", "PV.npvs", "category_ids", "deterministic_seed",
    },
    "cf.MergeSelectionMasks": {
        "mc_weight", "normalization_weight", "process_id", "category_ids", "cutflow.*",
    },
}))

# event weight columns
# config_2017.set_aux("event_weights", ["normalization_weight", "pu_weight"])
# event weight columns as keys in an ordered dict, mapped to shift instances they depend on
get_shifts = lambda *names: sum(([config_2017.get_shift(f"{name}_up"),
                                 config_2017.get_shift(f"{name}_down")] for name in names), [])
config_2017.x.event_weights = DotDict()
config_2017.x.event_weights["normalization_weight"] = []
config_2017.x.event_weights["pu_weight"] = get_shifts("minbias_xs")
#
# TODO: check that pdf/scale weights work for all cases
# for unc in ["mur", "muf", "scale", "pdf", "alpha"]:
#    config_2017.x.event_weights[unc] = get_shifts(unc)
# TODO: enable different cases for number of pdf/scale weights
# config_2017.set_aux("event_weights", ["normalization_weight", "pu_weight", "scale_weight", "pdf_weight"])

# versions per task family and optionally also dataset and shift
# None can be used as a key to define a default value
config_2017.set_aux("versions", {
})

# add categories
add_categories(config_2017)

# add variables
add_variables(config_2017)
