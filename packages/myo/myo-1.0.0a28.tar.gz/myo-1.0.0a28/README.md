# myo

# Components

## command

### RPC

#### `:MyoAddVimCommand`



#### `:MyoAddSystemCommand`



#### `:MyoAddShellCommand`



#### `:MyoRun`



#### `:MyoRunLine`



#### `:MyoRerun`



#### `:MyoParse`



#### `:MyoCurrentEventJump`



#### `:MyoQuitOutput`



#### `:MyoPrevEvent`



#### `:MyoNextEvent`



#### `:MyoVimTest`



#### `:MyoKill`



#### `:MyoReboot`



#### `:MyoHistory`



#### `:MyoTestDetermineRunner`



#### `:MyoTestExecutable`



#### `:MyoTestBuildPosition`



#### `:MyoTestBuildArgs`




## core

### RPC

#### `:MyoInit`



#### `:MyoInfo`



#### `:VimLeave`




## tmux

### RPC

#### `:MyoTmuxRender`



#### `:MyoTmuxInfo`



#### `:MyoTmuxQuit`




## ui

### RPC

#### `:MyoCreatePane`

Configure a new pane that can be spawned with `MyoOpenPane`.
`layout: <class 'chiasma.util.id.Ident'>` containing layout name
`ident: amino.maybe.Maybe[chiasma.util.id.Ident]` name to be used for commands like MyoOpenPane
`min_size: amino.maybe.Maybe[int]` minimum size integer
`max_size: amino.maybe.Maybe[int]` maximum size integer
`fixed_size: amino.maybe.Maybe[int]` fixed size, combination of min and max
`minimized_size: amino.maybe.Maybe[int]` size after calling MyoMinimizePane
`weight: amino.maybe.Maybe[float]` amount of growth this pane gets when there is space left above the minimums
`position: amino.maybe.Maybe[int]` absolute position in the layout
`minimized: amino.maybe.Maybe[bool]` whether to create the pane in minimized state

#### `:MyoOpenPane`



#### `:MyoClosePane`



#### `:MyoTogglePane`



#### `:MyoMinimizePane`



#### `:MyoKillPane`



#### `:MyoToggleLayout`



#### `:MyoUiInfo`



#### `:MyoFocus`




## vim

### RPC


# Settings

## `g:myo_tmux_watcher_interval`

tmux process polling interval

Tmux panes can be observed for events, like processes terminating.
This specifies the polling interval.


## `g:myo_tmux_socket`

tmux socket path

The tmux server can be chosen by its socket path. This is mainly intended for tests.


## `g:myo_vim_tmux_pane`

vim tmux pane id

Skip discovery of the tmux pane hosting neovim by its process id and use the supplied pane id
instead. Particularly helpful for tests.


## `g:myo_display_parse_result`

display parse result

After parsing the output of an executed command, display errors in a scratch buffer.


## `g:myo_auto_jump`

jump when changing output events

When loading the output buffer or cycling through output events, jump to the code location without
hitting the jump key.


## `g:test#filename_modifier`

vim-test filename modifier

A vim-test setting that is applied to file names.


## `g:myo_init_default_ui`

initialize vim and make panes

Create space, window, layout and pane for vim and the default execution target at startup.
The default target pane will be positioned to the right of vim.


## `g:myo_test_ui`

ui for running tests

Tests run with vim-test will be executed in this ui. Can be `tmux` or `internal`.


## `g:myo_test_pane`

pane for running tests

Tests run with vim-test will be executed in this pane.
Defaults to `make`.


## `g:myo_test_langs`

parsing langs for vim-test output

When parsing the output of a command executed with `MyoVimTest`, these languages are expected.


## `g:myo_load_history`

load command history

The history of executed commands is persisted to disk. This setting controls whether it is
restored on startup.


## `g:myo_builtin_output_config`

use default output configs

Command output parsing can be configured from multiple sources. If this setting is
`true`, myo's built-in configuration is used in addition to command-specific config.


## `g:myo_test_shell`

shell for running tests

Tests run with vim-test will be executed in this shell.
Takes precedence over `test_pane`.


## `g:myo_vim_pane_geometry`

geometry overrides for the vim pane

The vim pane is autodetected and -created, so its size, weight and position can be
overridden here. The format is:
```{
  "min_size": 50,
  "max_size": 50,
  "fixed_size": 50,
  "minimized_size": 50,
  "weight": 0.5,
  "position": 50,
}
```
Since the vim pane is wrapped in a vertical layout, these settings are actually applied to that, not the pane itself.
All settings are optional; the default is a weight of 0.5.

