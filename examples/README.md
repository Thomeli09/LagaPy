# Examples

`run_lagamine.py` demonstrates the **implemented** subprocess runner; it needs
real Lagamine input files and executable paths from your installation. It
does not create finite element inputs automatically.

```powershell
python examples/run_lagamine.py --lag model.LAG --dat model.DAT `
  --prepro C:\LagaProgs\Prepro.exe --lagamine C:\LagaProgs\Lagamine.exe `
  --workdir C:\Simulations\case01
```

To only prepare a batch file, add `--batch run_case.bat`. To run Prepro only,
add `--preprocess-only`; for only Lagamine, add `--solve-only`. For separate logging levels, use `--console-level WARNING --file-level DEBUG`
with `--log-file logs/case.log`, or `--no-console` for file-only logs.
For all options, run `python examples/run_lagamine.py --help`.

For further path, logging and timeout details see
[execution documentation](../docs/EXECUTION.md).
