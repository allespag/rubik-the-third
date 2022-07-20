"""
This type stub file was generated by pyright.
"""

def alive_bar(total=..., *, calibrate=..., **options): # -> _GeneratorContextManager[Unknown]:
    """An alive progress bar to keep track of lengthy operations.
    It has a spinner indicator, elapsed time, throughput and ETA.
    When the operation finishes, a receipt is displayed with statistics.

    If the code is executed in a headless environment, ie without a
    connected tty, all features are disabled but the final receipt.

    Another cool feature is that it tracks the actual count in regard of the
    expected count. So it will look different if you send more (or less) than
    expected.

    Also, the bar installs a hook in the system print function that cleans
    any garbage out of the terminal, allowing you to print() effortlessly
    while using the bar.

    Use it like this:

    >>> from alive_progress import alive_bar
    ... with alive_bar(123, 'Title') as bar:  # <-- expected total and bar title
    ...     for item in <iterable>:
    ...         # process item
    ...         bar()  # makes the bar go forward

    The `bar()` method should be called whenever you want the bar to go forward.
    You usually call it in every iteration, but you could do it only when some
    criteria match, depending on what you want to monitor.

    While in a progress bar context, you have two ways to output messages:
      - the usual Python `print()` statement, which will properly clean the line,
        print an enriched message (including the current bar position) and
        continue the bar right below it;
      - the `bar.text('message')` call, which sets a situational message right within
        the bar, usually to display something about the items being processed or the
        phase the processing is in.

    If the bar is over or underused, it will warn you!
    To test all supported scenarios, you can do this:
    >>> for x in 1000, 1500, 700, 0:
    ...    with alive_bar(x) as bar:
    ...        for i in range(1000):
    ...            time.sleep(.005)
    ...            bar()
    Expected results are these (but you have to see them in motion!):
|████████████████████████████████████████| 1000/1000 [100%] in 6.0s (167.93/s)
|██████████████████████████▋⚠            | (!) 1000/1500 [67%] in 6.0s (167.57/s)
|████████████████████████████████████████✗ (!) 1000/700 [143%] in 6.0s (167.96/s)
|████████████████████████████████████████| 1000 in 5.8s (171.91/s)

    Args:
        total (Optional[int]): the total expected count
        calibrate (float): maximum theoretical throughput to calibrate animation speed
        **options: custom configuration options, which override the global configuration:
            title (Optional[str]): an optional, always visible bar title
            length (int): the number of characters to render the animated progress bar
            spinner (Union[None, str, object]): the spinner style to be rendered next to the bar
                accepts a predefined spinner name, a custom spinner factory, or None
            bar (Union[None, str, object]): the bar style to be rendered in known modes
                accepts a predefined bar name, a custom bar factory, or None
            unknown (Union[str, object]): the bar style to be rendered in the unknown mode
                accepts a predefined spinner name, or a custom spinner factory (cannot be None)
            theme (str): a set of matching spinner, bar and unknown
                accepts a predefined theme name
            force_tty (Optional[int|bool]): forces a specific kind of terminal:
                False -> disables animations, keeping only the the final receipt
                True -> enables animations, and auto-detects Jupyter Notebooks!
                None (default) -> auto select, according to the terminal/Jupyter
            disable (bool): if True, completely disables all output, do not install hooks
            manual (bool): set to manually control the bar position
            enrich_print (bool): enriches print() and logging messages with the bar position
            receipt (bool): prints the nice final receipt, disables if False
            receipt_text (bool): set to repeat the last text message in the final receipt
            monitor (bool|str): configures the monitor widget `152/200 [76%]`
                send a string with `{count}`, `{total}` and `{percent}` to customize it
            elapsed (bool|str): configures the elapsed time widget `in 12s`
                send a string with `{elapsed}` to customize it
            stats (bool|str): configures the stats widget `(123.4/s, eta: 12s)`
                send a string with `{rate}` and `{eta}` to customize it
            monitor_end (bool|str): configures the monitor widget within final receipt
                same as monitor, the default format is dynamic, it inherits monitor's one
            elapsed_end (bool|str): configures the elapsed time widget within final receipt
                same as elapsed, the default format is dynamic, it inherits elapsed's one
            stats_end (bool|str): configures the stats widget within final receipt
                send a string with `{rate}` to customize it (no relation to stats)
            title_length (int): fixes the title lengths, or 0 for unlimited
                title will be truncated if longer, and a cool ellipsis "…" will appear at the end
            spinner_length (int): forces the spinner length, or `0` for its natural one
            refresh_secs (int): forces the refresh period, `0` for the reactive visual feedback
            ctrl_c (bool): if False, disables CTRL+C (captures it)
            dual_line (bool): if True, places the text below the bar

    """
    ...

class _Widget:
    def __init__(self, func, value, default) -> None:
        ...
    
    def __call__(self):
        ...
    


class _GatedProperty:
    def __set_name__(self, owner, name): # -> None:
        ...
    
    def __get__(self, obj, objtype=...): # -> Any | ((*_args: Unknown, **_kwargs: Unknown) -> None):
        ...
    
    def __set__(self, obj, value):
        ...
    


class _GatedAssignProperty(_GatedProperty):
    def __set__(self, obj, value): # -> None:
        ...
    


class __AliveBarHandle:
    pause = ...
    current = ...
    text = ...
    title = ...
    def __init__(self, pause, get_current, set_title, set_text) -> None:
        ...
    
    def __call__(self, *args, **kwargs): # -> None:
        ...
    


def alive_it(it, total=..., *, finalize=..., calibrate=..., **options):
    """New iterator adapter in 2.0, which makes it simpler to monitor any processing.

    Simply wrap your iterable with `alive_it`, and process your items normally!
    >>> from alive_progress import alive_it
    ... import time
    ... items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ... for item in alive_it(items):
    ...     time.sleep(.5)  # process item.

    And the bar will just work, it's that simple!

    All `alive_bar` parameters apply as usual, except `total` (which is smarter: if not supplied
    it will be inferred from the iterable using len or length_hint), and `manual` (which can't
    be used in this mode at all).
    To force unknown mode, even when the total would be available, send `total=0`.

    If you want to use other alive_bar's more advanced features, like for instance setting
    situational text messages, you can assign it to a variable! And send a `finalize` closure
    to set the final receipt title and/or text!

    >>> from alive_progress import alive_it
    ... bar = alive_it(items):
    ... for item in bar:
    ...     bar.text(f'Wow, it works! Item: {item}')
    ...     # process item.

    Args:
        it (iterable): the input iterable to be processed
        total: same as alive_bar
        finalize: a function to be called when the bar is going to finalize
        calibrate: same as alive_bar
        options: same as alive_bar

    See Also:
        alive_bar

    Returns:
        Generator

    """
    ...

class __AliveBarIteratorAdapter:
    def __init__(self, it, finalize, inner_bar) -> None:
        ...
    
    def __iter__(self): # -> Generator[Unknown, None, None]:
        ...
    
    def __call__(self, *args, **kwargs):
        ...
    
    def __getattr__(self, item): # -> Any:
        ...
    
    def __setattr__(self, key, value): # -> None:
        ...
    


