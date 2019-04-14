# How to add a new tool?

## Create a IaaS instance on the cloud 

If you are working in Norway and at the University of Oslo, Tromso or Bergen, see documentation at [IaaS](http://docs.uh-iaas.no/en/latest/).

## Test a tool with planemo

~~~`bash`
planemo t --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~

## Serve galaxy-tools with planemo

~~~`bash`
planemo s --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~
