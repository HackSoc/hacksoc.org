---
hostname: klaxon
fqdn: klaxon.hacksoc.org
name: hacksoc-grp
---

A plain-text version of this README can be found on grp@klaxon.hacksoc.org:~/README.markdown.

hacksoc-grp (pronounced "HackSoc Group"), or simply grp, is a collection of software maintained by HackSoc for use with the ITS linux machines, which would not otherwise be provided: more up-to-date packages, things which aren't strictly course-related, that sort of thing. All packages are built with a prefix of /tmp/hacksoc-grp.

You can see all packages which have been installed by listing /tmp/hacksoc-grp/packages.

## Mounting
You can mount grp with the following script. It may be helpful to save it to ~/grp.sh, and then source it to both mount grp and update your environment simultaneously.

```bash
GRPDIR=/tmp/hacksoc-grp

if [[ ! -e $GRPDIR/bin ]]; then
    mkdir -p $GRPDIR
    sshfs -o reconnect grp@klaxon.hacksoc.org: $GRPDIR
fi

export PATH=$GRPDIR/bin:$PATH
export LD_LIBRARY_PATH=$GRPDIR/lib:$LD_LIBRARY_PATH
```

**Health Warning:** Do not put this in your shell profile, as then if SSHFS hangs you won't be able to open a shell, which would be bad.

**Second Health Warning:** After executing this, your environment will be changed. Interaction with executables on the host system may change. So, instead of running the export lines of the script, you could just mount grp and then use a function like this to set up your environment for individual commands:

```bash
function grprun() {
    local GRPDIR=/tmp/hacksoc-grp
    PATH=$GRPDIR/bin:$PATH \
    LD_LIBRARY_PATH=$GRPDIR/lib:$LD_LIBRARY_PATH \
    $*
}
```

## Adding Packages
**For normal people:** email us, ping us on IRC, whatever.

**For people with access to klaxon, or those feeling particularly helpful:** grp is based on GNU Stow, a tool for managing hierarchies of symlinks. Packaging something consists in writing a script which will build it, and supply any necessary options to stow when it is installed.

For example, Isabelle 2015:

```bash
pkgname=isabelle2015
stow_opts="--ignore=ANNOUNCE --ignore=CONTRIBUTORS --ignore=COPYRIGHT --ignore=NEWS --ignore=README --ignore=ROOTS"

function build() {
    wget "https://www.cl.cam.ac.uk/research/hvg/Isabelle/dist/Isabelle2015_linux.tar.gz"
    tar xf Isabelle2015_linux.tar.gz
    mv Isabelle2015 $PKGDIR
}
```

Firstly, the package is given a name, this influences where is is installed. There are some pre-determined environmental variables:

 - $GRPDIR, the path of grp, /tmp/hacksoc-grp by default.
 - $STOWDIR, the directory managed by stow, $GRPDIR/packages by default.
 - $PKGDIR, the installation path of the package, $STOWDIR/$pkgname by default.

$STOWDIR/.. must be $GRPDIR, as otherwise stow will use symlink paths that don't work so nicely over sshfs.

Secondly, options to stow are provided. Typically this field should be empty, or consist only of a list of file exclusions.

Finally, a function to build the package is produced. This is a binary distribution of Isabelle 2015, so all that needs to happen here is to extract the tarball to the right place.

A package will be built when it is first installed, after that uninstall.sh and install.sh will only add or remove symlinks, to prevent repeating work needlessly.

A more complex build function is used in the z3-4.4.1 package:

```bash
function build() {
    wget "https://github.com/Z3Prover/z3/archive/z3-4.4.1.tar.gz"
    tar xf "z3-4.4.1.tar.gz"
    cd z3-z3-4.4.1

    # Make
    python2 scripts/mk_make.py
    cd build
    make

    # Install
    cd ..
    python2 scripts/mk_make.py --prefix=$PKGDIR
    cd build
    make install
    mv "$PKGDIR/lib/python2.7/dist-packages" "$PKGDIR/lib/python2.7/site-packages"
    rm "$PKGDIR/lib/python2.7/site-packages/libz3.so"
    ln -s ../../libz3.so "$PKGDIR/lib/python2.7/site-packages/libz3.so"
}
```

This is a source distribution of z3, so it needs to be compiled first. If you're not sure how to compile something, check if there is an Arch package in the [repositories](https://www.archlinux.org/packages) or the [AUR](https://aur.archlinux.org/). Arch PKGBUILD files are easy to read and somebody else has already figured out all the build system quirks for you.

## Sponsorship
This server has been very kindly given to us by Bytemark, who are a wonderful company and you should definitely check them out.

[![Bytemark](https://runciman.hacksoc.org/bytemark_logo_411_x_31.png)](https://www.bytemark.co.uk/r/hacksoc)