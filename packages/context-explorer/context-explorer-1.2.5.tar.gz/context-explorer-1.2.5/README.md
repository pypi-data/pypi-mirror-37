Thanks for stopping by! `（ ^_^）o自自o（^_^ ）`

**Note** The package installation name has changed to `context-explorer`
(hyphen) and the command to run the program is now `ctexplorer`. Previously
both of these were `context_explorer` (underline).

# Context-explorer

Context-explorer facilitates analyses and visualization of data extracted from
microscope images of cells.

## Relevance

The analyses methods in Context-explorer focuses on how populations of cells
are affected by their microenvironment, including local variations in cell
signalling and cell density. It is currently difficult for scientists without
previous programming experience to quantify these variables, although it is
relevant for many research areas. Facilitating this type of analyses can help
scientists around the world to improve their understanding of cellular behavior
and accelerate their research.

## Overview

![Workflow overview](doc/img/fig1-overview.png)

Context-explorer is controlled via a graphical user interface and aims to
enable powerful analysis and visualizations of single cell data extracted from
microscope images for a broad scientific audience. Context-explorer can work in
tandem with many other tools since it only depends on a correctly formatted
CSV-file as input and only outputs commonly used file formats (`.csv`, `.jpg`,
`.png`, and `.pdf`)


## Installation

Context-explorer can be installed via the package managers `conda` or `pip`, or
via the source code on GitLab. The recommended way is to use `conda`. To get
started, first download and install the [Anaconda Python
distribution](https://www.anaconda.com/download/) (version 3.x). This will
install Python together with common Python packages used for scientific
computing and the `conda` package manager. Proceed to use `conda` from either
the graphical program `Anaconda Navigator` or the command line:

### Anaconda Navigator

1. Open the `Anaconda Navigator` by searching for it in the start menu.
2. Click the `Channels` button and add "joelostblom" as a new channel.
3. Use the navigation pane on the left to switch to the `Environments` tab.
4. Change the dropdown meny from "installed" to "all" to see packages not yet
   installed on your system.
5. Search for "context-explorer"
6. Click the checkbox on the left and select "Mark for installation".
7. Hit `Apply` in the bottom right corner and click through the dialog to
   install `context-explorer`.
8. To run the program, open the `Anaconda Prompt` from the start menu (or the
   terminal on OS X and Linux), type in `ctexplorer` and hit enter.


### Command line

1. If you are using Windows, open up the `Anaconda Prompt` from the start menu.
   On MacOS and Linux you can use your default terminal (e.g. `terminal.app` on
   MacOS) instead of the `Anaconda Prompt`.
2. Type `conda install -c joelostblom context-explorer` and press enter.
3. After the installation has finished, run the program by typing `ctexplorer`
   and hitting enter.

### Updates using `conda`

#### Anaconda Navigator

Click the same checkbox as during installation and select "Mark for update",
then hit apply in the bottom right corner.

#### Command line

`conda update context-explorer`

## Using Context-explorer

If you are new to context-explorer, first download [the sample
data](https://gitlab.com/stemcellbioengineering/context-explorer/raw/master/sample-data/ce-sample.csv)
(right click link -> Save as). Launch context-explorer by typing `ctexplorer`
in the terminal/`Anaconda Prompt`, then choose the sample file (or your own
data) from the file selector. That's all you need to start testing
context-explorer!

Keep an eye on the terminal window for the output messages from
context-explorer. Detailed documentation and workflow examples are available at
the [documentation page](http://contextexplorer.readthedocs.io/en/latest/).
There is also [a brief video tutorial](https://vimeo.com/295958949) of how to
use the software.

## Support

If you run into troubles, please [check the issue
list](https://gitlab.com/stemcellbioengineering/context-explorer/issues) to see
if your problem has already been reported. If not, open a new issue or [ask for
help in the gitter chat](https://gitter.im/context_explorer/Lobby).

## Contributions

Feedback and suggestions are always welcome! This does not have to be
code-related, don't be shy =) Please read [the contributing
guidelines](https://gitlab.com/joelostblom/context-explorer/blob/master/CONTRIBUTING.md)
to get started.

## Roadmap

An overview of the projects direction is available in [the project
wiki](https://gitlab.com/stemcellbioengineering/context-explorer/wikis/Roadmap).

## Code of conduct

Be welcoming, friendly, and patient; be direct and respectful; understand and
learn from disagreement and different perspectives; lead by example; ask for
help when unsure; give people the benefit of the doubt; a simple apology can go
a long way; be considerate in the words that you choose. Detailed descriptions
of these points can be found in
[`CODE_OF_CONDUCT.md`](https://gitlab.com/stemcellbioengineering/context-explorer/blob/master/CODE_OF_CONDUCT.md).

## Known issues

Error output:

```
objc[42840]: Class FIFinderSyncExtensionHost is implemented in both
/System/Library/PrivateFrameworks/FinderKit.framework/Versions/A/FinderKit
(0x7fff9d6a3c90) and
/System/Library/PrivateFrameworks/FileProvider.framework/OverrideBundles/FinderSyncCollaborationFileProviderOverride.bundle/Contents/MacOS/FinderSyncCollaborationFileProviderOverride
(0x1c279d2cd8). One of the two will be used. Which one is undefined. ```
```

Solution:

This error is unrelated to CE and appears to origin from the Finder software in
MacOS as discussed
[here](https://stackoverflow.com/questions/46999695/class-fifindersyncextensionhost-is-implemented-in-both-warning-in-xcode-si)
and [here](https://github.com/lionheart/openradar-mirror/issues/17659). It shows
up because CE uses the Qt file dialog to pick the input file.
