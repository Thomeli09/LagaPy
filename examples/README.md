# Examples

Runnable finite element examples will be added **after** readers, writers and
the external Lagamine runner have been implemented and tested.

Planned examples include importing a small `.lag` mesh, generating boundary
conditions, writing an input set, running an externally installed solver,
and plotting selected output fields. Examples requiring Lagamine will be
clearly marked and will not be run as part of standard unit tests.

For now, verify the package foundation with:

```bash
python -c "import lagapy; print(lagapy.__version__)"
```
