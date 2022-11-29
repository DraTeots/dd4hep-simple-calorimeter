#include <vector>
#include <string>

#include <CLI11.hpp>

#include <StringHelpers.hh>
#include <spdlog/fmt/fmt.h>
#include <spdlog/spdlog.h>
#include "ArgumentProcessor.hh"


UserArguments InputProcessor::Process(int argc, char **argv)
{
    UserArguments result;                                          // This function result
    CLI::App app{mAppDescription};

    bool optShowGui = false;
    int optThreads = 1;
    std::string optVerbose("info");
    std::string optOutputName("g4e_output");
    std::vector<std::string> optAllFiles;
    app.add_flag("-g,--gui", optShowGui, "Shows Geant4 GUI");
    app.add_option("-o,--output", optOutputName, "Base name for Output files");
    app.add_option("-t,-j,--threads,--jobs", optThreads, "Number of threads. Single threaded mode if 0 or 1", 1);
    app.add_option("-v,--verbose", optVerbose,
                   "Verbosity 0-5 or: off fatal error warn info debug trace. '-v' (no val) means 'debug'. Can be set with /g4r/logLevel", "info");
    app.add_option("files", optAllFiles, "Input files. Macros (.mac) or generator files");

    // Parse everything
    try {
        app.parse(argc, argv);
    } catch(const CLI::ParseError &e) {
        app.exit(e);
        throw;
    }

    //
    // Input files (macros and data files)
    result.AllFileNames = optAllFiles;
    ProcessFileNames(result);                               // Separate file names as macro / data files
    if(result.MacroFileNames.empty()) {
        // TODO interactive terminal mode
        InputProcessor::PrintNoMacroHelp();
        exit(0);
    }

    //
    // Open GUI?:
    result.ShowGui = optShowGui;
    fmt::print("ARG:ShowGui = {}\n", result.ShowGui);

    //
    // Number of threads
    result.ThreadsCount = optThreads;
    fmt::print("ARG:ThreadsCount = {}\n", result.ThreadsCount);

    // Output file name:
    result.OutputBaseName = optOutputName;

    // G4E_MACRO_PATH
    const char* macroPathCstr = std::getenv("G4E_MACRO_PATH");
    ProcessMacroPath(result, macroPathCstr);

    return result;
}


void InputProcessor::ProcessFileNames(UserArguments &result) {
    // Separate filenames to Mac and other files
    for(const auto& name: result.AllFileNames) {
        if(g4e::EndsWith(name, ".mac")) {
            result.MacroFileNames.push_back(name);
        } else {
            result.SourceFileNames.push_back(name);
        }
    }

    // Print file names if apply
    if(!result.MacroFileNames.empty()) {
        fmt::print("ARG:Macro files:\n");
        for(const auto& fileName: result.MacroFileNames) {
            fmt::print("   {}\n", fileName);
        }
    }

    // Source file names:
    if(!result.MacroFileNames.empty()) {
        fmt::print("ARG:Source files:\n");
        for(const auto& fileName: result.SourceFileNames) {
            fmt::print("   {}\n", fileName);
        }
    }
}


void InputProcessor::ProcessMacroPath(UserArguments &result, const char *macroPathCstr) {
    result.IsSetMacroPath = macroPathCstr != nullptr;
    result.MacroPath = macroPathCstr? macroPathCstr: "";

    // Add JLeic detector to default Macro Path
    std::vector<std::string> paths;
    if(result.IsSetMacroPath) {
        result.MacroPath += ":"+result.ResourcePath+"/reference_detector";
    } else {
        result.MacroPath = result.ResourcePath+"/reference_detector";
    }
    fmt::print("ENV:G4E_MACRO_PATH:  is-set={}, value='{}'",  result.IsSetMacroPath, result.MacroPath );

}

std::string InputProcessor::mAppDescription =
        "g4e - Geant 4 Electron Ion Collider - is a full simulation part of ESCalate framework.";

void InputProcessor::PrintNoMacroHelp() {
    fmt::print(mAppDescription + "\n\n"
        "There is no macro files provided. Please look at "
        "$G4E_HOME/examples folder macros examples or how to run g4e from python\n"
        "You can get more help here: \n"
        "https://g4e.readthedocs.io/\n"
        "https://geant4.web.cern.ch/\n\n");
}