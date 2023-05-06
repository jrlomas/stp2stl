
# STP2STL

A utility written in python3 to convert STEP files to STLs.  The project depends on cadquery, and its derived dependencies. 

## Install it from command line using git on a virtual environment on Ubuntu / Debian

```bash
cd
sudo apt install python3 python3-venv
python3 -m venv ~/.venv/stp2stl
source ~/.venv/stp2stl/bin/activate
pip install --upgrade pip
git clone https://github.com/jrlomas/stp2stl
cd stp2stl
pip install build
python -m build
pip install ./dist/stp2stl-0.0.1-py3-none-any.whl
```

## Usage

You can find an example export.json file [here](https://github.com/jrlomas/stp2stl/blob/master/examples/export.json).  For completeness here it is inline:
```json
{
    "filename" : "./sample.step",
    "stl_filepath" : "./stl",
    "components" : [{"component" : "Leaf1",
                     "rotations" : [{ "axis" : "y", "degrees" : -90}],
                     "stl_filename" : "leaf1.stl"},

                    {"component" : "Leaf2",
                     "rotations" : [{"axis" : "x", "degrees" : -90}],
                     "stl_filename" : "leaf2.stl"}
        ]
}
```

``filename`` in export.json is the name of the step file you want to use to create the STLs, the filename path is relative to the current working directory.

``stl_filepath`` refers to the directory where to place the created STLs.  If the path does not 
exist, a new directory will be created.

Under ``components`` one can define each one of the STLs to export.  The ``component`` name must match exactly the name of the component, also know and PRODUCT in the STEP nomenclature, in the CAD application that export the STEP file; otherwise, the script will fail.

``rotations`` can be performed in the "x", "y', or "z" axis and are not exclusive (i.e. one can rotate in each one of the axis, the rotation operations are performed in the order provided).

``stl_filename`` is the name of the stl file to write under the ``stl_filepath`` provided.

Now try the script:

```bash
$ cd ~/stp2stl/examples
$ stp2stl export.json
```

## Support

As the script is quite new currently, any error please do report them under issues.

## License

Read the [MIT LICENSE](LICENSE.md) file.