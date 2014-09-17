# Auto generated configuration file
# using: 
# Revision: 1.20 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions DES23_62_V1::All -n 10 --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,L1,DIGI2RAW --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023HGCalMuon --geometry Extended2023HGCalV4Muon,Extended2023HGCalV4MuonReco --magField 38T_PostLS1 --filein file:../EventGeneration/HGC/FourMuonEventsPt200GeV.root --fileout file:step2.root --pileup AVE_140_BX_25ns --pileup_input dbs:/RelValMinBias_TuneZ2star_14TeV/CMSSW_6_2_0_SLHC15-DES23_62_V1_UPGHGCalV4-v1/GEN-SIM
import FWCore.ParameterSet.Config as cms

process = cms.Process('DIGI2RAW')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2023HGCalV4MuonReco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1500)
)

# Input source
process.source = cms.Source("PoolSource",
                            secondaryFileNames = cms.untracked.vstring(),
                            #fileNames = cms.untracked.vstring('root://eoscms.cern.ch//store/user/khurana/HGCAL/GenSim/FourMuon200GeV/FourMuonEventsPt200GeV.root')
                            fileNames = cms.untracked.vstring('root://eoscms.cern.ch//store/user/khurana/HGCAL/GenSim/SingleParticle/INPUTFILE')
                            )

process.options = cms.untracked.PSet(
    
    )

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    fileName = cms.untracked.string('file:/tmp/khurana/OUTPUTFILE'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW')
    )
)

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(140.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_6_2_0_SLHC15/RelValMinBias_TuneZ2star_14TeV/GEN-SIM/DES23_62_V1_UPGHGCalV4-v1/00000/06EA8CB2-1106-E411-A0F3-00259059649C.root', '/store/relval/CMSSW_6_2_0_SLHC15/RelValMinBias_TuneZ2star_14TeV/GEN-SIM/DES23_62_V1_UPGHGCalV4-v1/00000/FE1431FE-0D06-E411-B748-0026189438B3.root'])
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'DES23_62_V1::All', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023HGCalMuon 

#call to customisation function cust_2023HGCalMuon imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023HGCalMuon(process)

# End of customisation functions
#process.mix.digitizers.hgceeDigitizer.digiCfg.mip2noise  = cms.double(10000.0)
process.mix.digitizers.hgceeDigitizer.digiCfg.shaperTau  = cms.double(TAUVALUE)
