#!/bin/sh

export DETECTOR=kak_bog_cherepahu
export DETECTOR_PATH=/usr/local/share/kak_bog_cherepahu
export DETECTOR_CONFIG=kak_bog_cherepahu
export DETECTOR_VERSION=main

export BEAMLINE=kak_bog_cherepahu
export BEAMLINE_PATH=/usr/local/share/kak_bog_cherepahu
export BEAMLINE_CONFIG=kak_bog_cherepahu
export BEAMLINE_VERSION=main

## note: we will phase out the JUGGLER_* flavor of variables in the future
export JUGGLER_DETECTOR=$DETECTOR
export JUGGLER_DETECTOR_CONFIG=$DETECTOR_CONFIG
export JUGGLER_DETECTOR_VERSION=$DETECTOR_VERSION
export JUGGLER_DETECTOR_PATH=$DETECTOR_PATH

export JUGGLER_BEAMLINE=$BEAMLINE
export JUGGLER_BEAMLINE_CONFIG=$BEAMLINE_CONFIG
export JUGGLER_BEAMLINE_VERSION=$BEAMLINE_VERSION
export JUGGLER_BEAMLINE_PATH=$BEAMLINE_PATH

## Export detector libraries
if [[ "$(uname -s)" = "Darwin" ]] || [[ "$OSTYPE" == "darwin"* ]]; then
	export DYLD_LIBRARY_PATH="/usr/local/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
else
	export LD_LIBRARY_PATH="/usr/local/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
