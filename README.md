# Galaxy Tools maintained by NordicESMHub

<img src="nordicESMHub_logo.png" width="100"/>

## Test a tool with planemo

~~~`bash`
planemo t --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~

## Serve galaxy-tools with planemo

~~~`bash`
planemo s --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~
