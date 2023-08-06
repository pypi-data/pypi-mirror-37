# Python Import Guardian README

## What is it?

`python-import-guardian` is a static-analysis import guardian for Python. It
can be used to control explictly which Python modules and packages can be
imported by a given set of modules and packages in your project.

## When is this useful?

Let's say you have a project with two major components — a client and a server.
Both of these components live in the same repository (for the sake of argument)
and both use a common set of shared code for various functions — for example to
determine how certain hashes are calculated or some such.

The code may be laid out thus:

    /myproject
      |
      |- client/
      |- server/
      |- shared/

Conceptually, you only ever want `client` and `shared` code to be installed on
client machines and `server` and `shared` code on server machines. Modules in
`client` and `server` may import from `shared`, but not from each other, and
`shared` may import from neither — this ensures that you have a good separation
of concerns between client and server code whilst maintaining some shared code
and good DRY principles.

`python-import-guardian` allows you to define how you want these modules to
relate to each other when it comes to which module can import what from where.
For our example project, a simple `importguardian.json` file at the top of the
project tree might look like this:

    {
        "forbidden_modules": {
            "server": [
                "client",
                "shared"
            ],
            "client": [
                "server",
                "shared"
            ]
            
        }
    }
    
The `forbidden_modules` declaration here maps Python modules to a list of the
modules or packages which may not import them. So in this case: `server` may
not be imported by `client` or `shared`, and `client` may not be imported by
`server` or `shared`. `forbidden_modules` is a blacklist, so `shared` can be
imported by anything because it isn't mentioned as a forbidden module.