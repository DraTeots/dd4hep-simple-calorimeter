//
// ************************************************************************
// * License and Disclaimer                                               *
// *                                                                      *
// * The	Geant4 software	is	copyright of the Copyright Holders	of      *
// * the Geant4 Collaboration.	It is provided	under	the terms	and       *
// * conditions of the Geant4 Software License,	included in the file      *
// * LICENSE and available at	http://cern.ch/geant4/license .	These       *
// * include a list of copyright holders.                                 *
// *                                                                      *
// * Neither the authors of this software system, nor their employing     *
// * institutes,nor the agencies providing financial support for this     *
// * work	make	any representation or	warranty, express or implied,       *
// * regarding	this	software system or assume any liability for its     *
// * use.	Please see the license in the file	LICENSE	and URL above       *
// * for the full disclaimer and the limitation of liability.             *
// *                                                                      *
// * This	code	implementation is the result of	the	scientific and        *
// * technical work of the GEANT4 collaboration.                          *
// * By using,	copying,	modifying or	distributing the software (or     *
// * any work based	on the software)	you	agree	to acknowledge its        *
// * use	in	resulting	scientific	publications,	and indicate your       *
// * acceptance of all terms of the Geant4 Software license.              *
// ************************************************************************
//

#include <CLHEP/Random/Random.h>
#include <CLHEP/Random/RanecuEngine.h>
#include "DetectorConstruction.hh"
#include <G4String.hh>
#include <G4Timer.hh>
#include <G4UIExecutive.hh>
#include <G4UImanager.hh>
#include "G4Utils.hh"
#include <G4VisExecutive.hh>
#include <G4VisManager.hh>
#include "MyVisCommands.hh"
#include "PhysicsListMessenger.hh"
#include <Randomize.hh>
#include "MyRunManager.hh"
#include <iostream>
#include <string>
#include <G4TrajectoryDrawByAttribute.hh>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/fmt.h>
#include <ArgumentProcessor.hh>


int main(int argc, char **argv) {
    using namespace fmt;

    spdlog::set_level(spdlog::level::debug);



    auto appArgs = InputProcessor::Process(argc, argv);



    // TODO: problems with MT mode. REplacing histograms in HistogramManager, Geometry test issues.
    //       therefore for now sticker to single threaded mode.
    G4RunManager *runManager = new MyRunManager();

    // Construct the detector
    runManager->SetUserInitialization(new DetectorConstruction());

    // Deferred instantiate physics list via the messenger (allows changing physics list, adding optical physics)
    new PhysicsListMessenger(runManager);

    // ActionInitialization is instantiated inside the PhysicsListMessenger because it needs to be instantiated
    // after the physics list which is instantiated deferred via macro command

    // Initialize visualization

    // Start timer
    G4Utils::getInstance()->startTimer();
    G4VisExecutive* visManager = nullptr;
    G4UIExecutive* uiExec = nullptr;
    std::string defaultMacro = "refdet.mac";     // No GUI default macro. Default macro is used if no other macros given

    // We show GUI if user didn't provided any macros of if he has --gui/-g flag
    if(appArgs.ShowGui) {
        appArgs.ShowGui = true;
        visManager = new G4VisExecutive;
        visManager->Initialize();
        uiExec = new G4UIExecutive(argc, argv);
    }

    // auto *ui = new G4UIExecutive(argc, argv);
    G4UImanager *ui = G4UImanager::GetUIpointer();

    // set macro path from environment if it is set
    ui->ApplyCommand(format("/control/macroPath {}", appArgs.MacroPath));

    // No Macros provided by user? Use default macro
    if (appArgs.MacroFileNames.empty()) {
        appArgs.MacroFileNames.push_back(defaultMacro);
    }

    // Execute all macros
    fmt::print("Executing macro files:");
    for(const auto& fileName: appArgs.MacroFileNames) {
        std::string command = "/control/execute " + fileName;
        fmt::print("   {}\n", command);
        std::cout << " exec command : " << command << std::endl;
        ui->ApplyCommand(command);
    }

    // We start visual mode if no files provided or if --gui flag is given
    if(appArgs.ShowGui && uiExec) {
        uiExec->SessionStart();
    }

//    if (!ui) {
//        // Batch mode
//        G4String command = "/control/execute ";
//        G4String fileName = argv[1];
//        UImanager->ApplyCommand(command + fileName);
//    } else {
//        // Interactive mode
//        // Instantiate Custom Visualization Messenger
//        new MyVisCommands();
//        ui->SessionStart();
//        delete ui;
//    }

    // Print elapsed time
    G4Utils::getInstance()->printTimer();

    delete visManager;
    delete runManager;

    return 0;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
