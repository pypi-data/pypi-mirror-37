=====================
 slapos.recipe.build
=====================

.. contents::

Examples
--------

Recipe to build the software.

Example buildout::

  [buildout]
  parts =
    script

  [script]
  # default way with using script
  recipe = slapos.recipe.build
  url_0 = http://host/path/file.tar.gz
  md5sum = 9631070eac74f92a812d4785a84d1b4e
  script =
    import os
    os.chdir(%(work_directory)s)
    unpack(%(url_0), strip_path=True)
    execute('make')
    execute('make install DEST=%(location)s')
  slapos_promise =
    directory:bin
    dynlib:bin/file linked:libz.so.1,libc.so.6,libmagic.so.1 rpath:${zlib:location}/lib,!/lib
    directory:include
    file:include/magic.h
    directory:lib
    statlib:lib/libmagic.a
    statlib:lib/libmagic.la
    dynlib:lib/libmagic.so linked:libz.so.1,libc.so.6 rpath:${zlib:location}/lib
    dynlib:lib/libmagic.so.1 linked:libz.so.1,libc.so.6 rpath:${zlib:location}/lib
    dynlib:lib/libmagic.so.1.0.0 linked:libz.so.1,libc.so.6 rpath:${zlib:location}/lib
    directory:share
    directory:share/man
    directory:share/man/man1
    file:share/man/man1/file.1
    directory:share/man/man3
    file:share/man/man3/libmagic.3
    directory:share/man/man4
    file:share/man/man4/magic.4
    directory:share/man/man5
    directory:share/misc
    file:share/misc/magic.mgc

  [multiarchitecture]
  recipe = slapos.recipe.build
  slapos_promise =
    ...
  x86 = http://host/path/x86.zip [md5sum]
  x86-64 =  http://host/path/x64.zip [md5sum]
  script =
    if not self.options.get('url'): self.options['url'], self.options['md5sum'] = self.options[guessPlatform()].split(' ')
    extract_dir = self.extract(self.download(self.options['url'], self.options.get('md5sum')))
    workdir = guessworkdir(extract_dir)
    self.copyTree(workdir, "%(location)s")

You can remove formatting by using option “format = no” (default is “yes”)

For example::

  [escaping]
  recipe = slapos.recipe.build
  example = foobar's one
  script =
    print('%%s' %% self.options['example'])
    # will print “foobar's one”

  [no-escaping]
  recipe = slapos.recipe.build
  example = foobar's one
  foo = bar
  format = no
  script =
    print('%s' % self.options['example'])
    # will print “foobar's one”
    print('%(foo)s')
    # will print “%(foo)s”

Pure download
~~~~~~~~~~~~~

Note: deprecated entry-point.

::

  [buildout]
  parts =
    download

  [download]
  recipe = slapos.recipe.build:download
  url = https://some.url/file

Such profile will download https://some.url/file and put it in
buildout:parts-directory/download/download

filename parameter can be used to change destination named filename.

destination parameter allows to put explicit destination.

md5sum parameter allows pass md5sum.

mode (octal, so for rw-r--r-- use 0644) allows to set mode

Exposes target attribute which is path to downloaded file.

Notes
-----

This recipe suffers from buildout download utility issue, which will do not
try to redownload resource with wrong md5sum.

==============================
 slapos.recipe.build:gitclone
==============================

Checkout a git repository.
Supports slapos.libnetworkcache if present, and if boolean 'use-cache' option
is true.

Examples
--------

Those examples use slapos.recipe.build repository as an example.

Simple clone
~~~~~~~~~~~~

Only `repository` parameter is required. For each buildout run,
the recipe will pick up the latest commit on the remote master branch::

  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... use-cache = true
  ... """)

This will clone the git repository in `parts/git-clone` directory.
Then let's run the buildout::

  >>> print(system(buildout))
  Installing git-clone.
  Cloning into '/sample-buildout/parts/git-clone'...

Let's take a look at the buildout parts directory now::

  >>> ls(sample_buildout, 'parts')
  d git-clone

When updating, it will do a "git fetch; git reset @{upstream}"::

  >>> print(system(buildout))
  Updating git-clone.
  Fetching origin
  HEAD is now at ...

Specific branch
~~~~~~~~~~~~~~~

You can specify a specific branch using `branch` option. For each
run it will take the latest commit on this remote branch::

  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... branch = build
  ... """)

Then let's run the buildout::

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  Installing git-clone.
  Cloning into '/sample-buildout/parts/git-clone'...

Let's take a look at the buildout parts directory now::

  >>> ls(sample_buildout, 'parts')
  d git-clone

And let's see that current branch is "build"::

  >>> import subprocess
  >>> cd('parts', 'git-clone')
  >>> print(subprocess.check_output(['git', 'branch'], universal_newlines=True))
  * build

When updating, it will do a "git fetch; git reset build"::

  >>> cd(sample_buildout)
  >>> print(system(buildout))
  Updating git-clone.
  Fetching origin
  HEAD is now at ...

Specific revision
~~~~~~~~~~~~~~~~~

You can specify a specific commit hash or tag using `revision` option.
This option has priority over the "branch" option::

  >>> cd(sample_buildout)
  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... revision = 2566127
  ... """)

Then let's run the buildout::

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  Installing git-clone.
  Cloning into '/sample-buildout/parts/git-clone'...

Let's take a look at the buildout parts directory now::

  >>> ls(sample_buildout, 'parts')
  d git-clone

And let's see that current revision is "2566127"::

  >>> import subprocess
  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], universal_newlines=True))
  2566127

When updating, it will do a "git fetch; git reset revision"::

  >>> cd(sample_buildout)
  >>> print(system(buildout))
  Updating git-clone.
  ...
  HEAD is now at 2566127 ... 
  ...
  <BLANKLINE>

Empty revision/branch
~~~~~~~~~~~~~~~~~~~~~

Specifying an empty revision or an empty branch will make buildout
ignore those values as if it was not present at all (allowing to easily
extend an existing section specifying a branch)::

  >>> cd(sample_buildout)
  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone-with-branch]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... revision = 2566127
  ...
  ... [git-clone]
  ... <= git-clone-with-branch
  ... revision =
  ... branch = master
  ... """)

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  Installing git-clone.
  Cloning into '/sample-buildout/parts/git-clone'...

  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('git branch'))
  * master

Revision/branch priority
~~~~~~~~~~~~~~~~~~~~~~~~

If both revision and branch parameters are set, revision parameters is used
and branch parameter is ignored::

  >>> cd(sample_buildout)
  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... branch = mybranch
  ... revision = 2566127
  ... """)

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  Installing git-clone.
  Warning: "branch" parameter with value "mybranch" is ignored. Checking out to revision 2566127...
  Cloning into '/sample-buildout/parts/git-clone'...
  HEAD is now at 2566127 ...

  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('git branch'))
  * master

Setup a "develop" repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to setup a repository that will be manually alterated over time for
development purposes, you need to make sure buildout will NOT alter it and NOT
erase your local modifications by specifying the "develop" flag::

  [buildout]
  parts = git-clone

  [git-clone]
  recipe = slapos.recipe.build:gitclone
  repository = https://example.net/example.git/
  develop = true

  >>> cd(sample_buildout)
  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... develop = true
  ... """)

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  Installing git-clone.
  Cloning into '/sample-buildout/parts/git-clone'...

Buildout will then keep local modifications, instead of resetting the
repository::

  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('echo foo > setup.py'))

  >>> cd(sample_buildout)
  >>> print(system(buildout))
  Updating git-clone.
  Fetching origin
  ...
  <BLANKLINE>


  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('cat setup.py'))
  foo

Then, when update occurs, nothing is done::

  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('echo kept > local_change'))

  >>> print(system('git remote add broken http://git.erp5.org/repos/nowhere'))
  ...

  >>> cd(sample_buildout)
  >>> print(system(buildout))
  Updating git-clone.
  Fetching origin
  Fetching broken
  Unable to update:
  Traceback (most recent call last):
  ...
  ...CalledProcessError: Command '['git', 'fetch', '--all']' returned non-zero exit status 1
  <BLANKLINE>
  ...
  fatal: unable to access 'http://git.erp5.org/repos/nowhere/': The requested URL returned error: 500
  error: Could not fetch broken
  <BLANKLINE> 
  
  >>> cd(sample_buildout, 'parts', 'git-clone')
  >>> print(system('cat local_change'))
  kept

In case of uninstall, buildout will keep the repository directory::

  >>> cd(sample_buildout)
  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = git-clone
  ...
  ... [git-clone]
  ... recipe = slapos.recipe.build:gitclone
  ... repository = http://git.erp5.org/repos/slapos.recipe.build.git
  ... develop = true
  ... # Triggers uninstall/install because of section signature change
  ... foo = bar
  ... """)

  >>> print(system(buildout))
  Uninstalling git-clone.
  Running uninstall recipe.
  You have uncommited changes in /sample-buildout/parts/git-clone. This folder will be left as is.
  Installing git-clone.
  destination directory already exists.
  ...
  <BLANKLINE>

Specific git binary
~~~~~~~~~~~~~~~~~~~

The default git command is `git`, if for a any reason you don't
have git in your path, you can specify git binary path with `git-command`
option.

Ignore SSL certificate
~~~~~~~~~~~~~~~~~~~~~~

By default, when remote server use SSL protocol git checks if the SSL
certificate of the remote server is valid before executing commands.
You can force git to ignore this check using `ignore-ssl-certificate`
boolean option::

  [buildout]
  parts = git-clone

  [git-clone]
  recipe = slapos.recipe.build:gitclone
  repository = https://example.net/example.git/
  ignore-ssl-certificate = true

Other options
~~~~~~~~~~~~~

shared
    Clone with ``--shared`` option if true. See ``git-clone`` command.

sparse-checkout
    The value of the `sparse-checkout` option is written to the
    ``$GITDIR/info/sparse-checkout`` file, which is used to populate the working
    directory sparsely. See the `SPARSE CHECKOUT` section of ``git-read-tree``
    command. This feature is disabled if the value is empty or unset.

Full example
~~~~~~~~~~~~

::

  [buildout]
  parts = git-clone

  [git-binary]
  recipe = hexagonit.recipe.cmmi
  url = http://git-core.googlecode.com/files/git-1.7.12.tar.gz

  [git-clone]
  recipe = slapos.recipe.build:gitclone
  repository = http://example.net/example.git/
  git-command = ${git-binary:location}/bin/git
  revision = 0123456789abcdef


=========================
 slapos.recipe.build:npm
=========================

Downloads and installs node.js packages using Node Package Manager (NPM).

Examples
--------

Basic example
~~~~~~~~~~~~~

Here is example to install one or several modules::

  [buildout]
  parts = node-package

  [node-package]
  recipe = slapos.recipe.build:npm
  modules =
    colors
    express

  # Optional argument specifying perl buildout part, if existing.
  # If specified, recipe will use the perl installed by buildout.
  # If not specified, will take the globally available perl executable.
  node = node-0.6

Specific version
~~~~~~~~~~~~~~~~
::

  [buildout]
  parts = node-package

  [node-package]
  recipe = slapos.recipe.build:npm
  modules =
    express@1.0.2
  node = node-0.6

==========================
 slapos.recipe.build:vm.*
==========================

This is a set of recipes to build Virtual Machine images and execute commands
inside them. They rely on QEMU and OpenSSH: executables are found via the PATH
environment variable. They do nothing on update.

Common options
--------------

location
    Folder where the recipe stores any produced file.
    Default: ${buildout:parts-directory}/<section_name>

environment
    Extra environment for the spawn executables. It can either be the name of a
    section or a list of variables (1 per line, in the form ``key=value``).
    Values are expanded with current environment using Python %-dict formatting.

mem
    Python expression evaluating to an integer that specifies the
    RAM size in MB for the VM.

smp
    Number of CPUs for the VM. Default: 1

Example
~~~~~~~

::

  [vm-run-environment]
  PATH = ${openssh:location}/bin:${qemu:location}/bin:%(PATH)s

  [vm-run-base]
  recipe = slapos.recipe.build:vm.run
  environment = vm-run-environment
  mem = 256 * (${:smp} + 1)
  smp = 4

slapos.recipe.build:vm.install-debian
-------------------------------------

Install Debian from an ISO image. Additional required binaries:

- ``7z`` (from 7zip), to extract kernel/initrd from the ISO;
- ``file``, which is used to test that the VM image is bootable.

Currently, it only produces `raw` images, in `discard` mode (see ``-drive``
QEMU option): combined the use of ``discard`` mount option, this minimizes
the used space on disk.

Options
~~~~~~~

location
    Produced files: ``<dist>.img`` (1 for each token of `dists`), ``passwd``
    and optionally ``ssh.key``

arch
    QEMU architecture (the recipe runs the ``qemu-system-<arch>`` executable).
    It is also used to select the ISO in the sections refered by `dists`.
    Default to host architecture.

dists
    List of VMs to build: each token refers to a buildout section name that
    describes the ISOs to use. See `ISO sections`_ below.
    Tokens can't contain `'.'` characters.

size
    Size of the VM image. This must be an integer, optionally followed by a
    IEC or SI suffix.

mem
    Default: 256

[<dist>/]preseed.<preseed>
    Set the <preseed> value for the installation. The recipe has many default
    preseed values: you can see the list in the ``InstallDebianRecipe.preseed``
    class attribute (file ``slapos/recipe/vm.py``). Aliases are recognized
    (but the recipe includes a mapping that may be out-of-date.).
    Any value except ``passwd/*`` can optionally be prefixed so that they only
    apply for a particular VM.

[<dist>/]debconf.<owner>
    List of debconf value for <owner> (usually a package name),
    each line with 2 whitespace-separated parts: <key> <value>.
    Like for preseed.* values, they can be specific to <dist>.

late-command
    Shell commands to execute at the end of the installation. They are run
    inside the target system. This is a reliable alternative to the
    ``preseed.preseed/late_command`` option. The ``DIST`` shell variable is
    set to the VM being built.

packages
    Extra packages to install.
    Like for `late-command`, do not use ``preseed.pkgsel/include``.
    If you want to install packages only for some specific <dist>, you can do
    it in ``late-command``, by testing ``$DIST`` and using
    ``apt-get install -y``.

vm.run
    Boolean value that is `true` by default, to configure the VM for use with
    the `slapos.recipe.build:vm.run`_ recipe:

    - make sure that the `ssh` and `sudo` packages are installed
    - an SSH key is automatically created with ``ssh-keygen``, and it can be
      used to connect as `root`

ISO sections
~~~~~~~~~~~~

<arch>.iso
    Name of the section that provides the ISO image, for example by downloading
    it. This section must define 2 options: `location` is the folder
    containing the ISO, and `filename` is the file name of the ISO.

<arch>.kernel
    Path to kernel image inside the ISO.

<arch>.initrd
    Path to initrd image inside the ISO.

User setup
~~~~~~~~~~

By default, there's no normal user created. Another rule is that a random
password is automatically generated if there is no password specified.

You have nothing to do if you only plan to use the VM with `vm.run`.

For more information about the ``passwd/*`` preseed values, you can look at
the ``user-setup-udeb`` package at
https://anonscm.debian.org/cgit/d-i/user-setup.git/tree/
and in particular the ``user-setup-ask`` and ``user-setup-apply`` scripts.

Example
~~~~~~~

::

  [vm-install-environment]
  # vm-run-environment refers to the section in common options
  PATH = ${file:location}/bin:${p7zip:location}/bin:${vm-run-environment:PATH}

  [vm-debian]
  recipe = slapos.recipe.build:vm.install-debian
  environment = vm-install-environment
  dists = debian-jessie debian-stretch
  size = 2Gi
  late-command =
  # rdnssd causes too much trouble with QEMU 2.7, because the latter acts as
  # a DNS proxy on both IPv4 and IPv6 without translating queries to what the
  # host supports.
    dpkg -P rdnssd
  debconf.debconf =
    debconf/frontend noninteractive
    debconf/priority critical
  # minimal size
  preseed.apt-setup/enable-source-repositories = false
  preseed.recommends = false
  preseed.tasks =

  [debian-jessie]
  x86_64.iso = debian-amd64-netinst.iso
  x86_64.kernel = install.amd/vmlinuz
  x86_64.initrd = install.amd/initrd.gz

  [debian-stretch]
  <= debian-jessie
  x86_64.iso = debian-amd64-testing-netinst.iso

  [debian-amd64-netinst.iso]
  ...

slapos.recipe.build:vm.run
--------------------------

Execute shell commands inside a VM, in snapshot mode (the VM image is not
modified).

``${buildout:directory}`` is always mounted as `/mnt/buildout` inside the VM.

Mount points use the 9p file-system. Make sure that:

- QEMU is built with --enable-virtfs;
- the VM runs a kernel that is recent enough (Debian Squeeze kernel 2.6.32 is
  known to fail, and you'd have to use the one from squeeze-backports).

Options
~~~~~~~

location
    Folder where to store any produce file. Inside the guest, it is pointed to
    by the PARTDIR environment variable. It is also used as temporary storage
    for changes to the VM image.

vm
    Folder containing the VM images and the `ssh.key`` file. See the `location`
    option of the `vm.install-*` recipes.

dist
    VM image to use inside the `vm` folder.

commands
    List of <command> options, each one being a shell script to execute via
    SSH. They are processed in sequence. This is usually only required if you
    want to reboot the VM. Default: command

mount.<name>
    Extra mount point. The value is a host folder that is mounted as
    ``/mnt/<name>``.

stop-ssh
    Tell `reboot` function how to stop SSH (see Helpers_).
    Default: systemctl stop ssh

user
    Execute commands with this user. The value can be ``root``. By default,
    it is empty and it means that:

    - a ``slapos`` user is created with the same uid/gid than the user using
      this recipe on the host, which can help accessing mount points;
    - sudo must be installed and the created user is allowed to become root
      without password.

    In any case, SSH connects as root.

wait-ssh
    Time to wait for (re)boot. The recipe fails if it can't connect to the SSH
    server after this number of seconds. Default: 60

Helpers
~~~~~~~

Before commands are executed, all `mount.<name>` are mounted
and a few helpers are set to make scripting easier.

set -e
    This is done before anything else, to make buildout abort if any untested
    command fails.

reboot
    Function to safely reboot the guest. The next command in `commands` will be
    executed once the SSH server is back.

map <host_path>
    Function to map a folder inside ``${buildout:directory}``.

PARTDIR
    Folder where to store any produced file. Inside the guest, it actually
    maps to `location` on the host. This is useful because you can't write
    ``PARTDIR=`map ${:location}``` if you don't explicitly set `location`.

Example
~~~~~~~

::

  [vm-run-base]
  # extends above example in common options
  vm = ${vm-debian:location}
  dist = debian-jessie

  [vm-debian]
  # extends above example in vm.install-debian
  packages += build-essential devscripts equivs git

  [userhosts-repository]
  recipe = slapos.recipe.build:gitclone
  repository = https://lab.nexedi.com/nexedi/userhosts.git
  # we don't need a working directory on the host
  sparse-checkout = /.gitignore

  [build-userhosts-map]
  <= vm-run-base
  repository = `map ${userhosts-repository:location}`
  command =
    git clone -s ${:repository} userhosts
    cd userhosts
    mk-build-deps -irs sudo -t 'apt-get -y'
    dpkg-buildpackage -uc -b -jauto
    cd ..
    mv *.changes *.deb $PARTDIR

  # Alternate way, which is required if [userhosts-repository] is extended
  # in such way that the repository is outside ${buildout:directory}.
  [build-userhosts-mount]
  <= build-userhosts-map
  mount.userhosts = ${userhosts-repository:location}
  repository = /mnt/userhosts

  [test-reboot]
  <= vm-run-base
  commands = hello world
  hello =
    uptime -s
    echo Hello ...
    reboot
  world =
    uptime -s
    echo ... world!
