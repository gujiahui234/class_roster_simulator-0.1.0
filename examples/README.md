# Runnable example

Install the package, then run the starter program from the repository root:

```powershell
python -m pip install -e .
python examples\basic_roster.py
```

You can customize it without editing the file:

```powershell
python examples\basic_roster.py --size 5 --seed 2026 `
  --birth-start 2008-09-01 --birth-end 2010-08-31
```

The script is intentionally structured around a typed `main()` function so it can be copied as a small application scaffold.
