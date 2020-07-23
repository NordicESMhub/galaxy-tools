# How to add a new tool?

## On which platform should you develop your new tool?

### Create a Virtual Machine (IaaS)

If you are working in Norway and at the University of Oslo, Tromso or Bergen, see documentation at [IaaS](http://docs.uh-iaas.no/en/latest/).

Then install [planemo](https://planemo.readthedocs.io/en/latest/).


### Use Planemo OVA image

See [Planemo Virtual Appliance documentation](https://planemo.readthedocs.io/en/latest/appliance.html).

## Develop a tool 

Best practices for developing new tools are [https://galaxy-iuc-standards.readthedocs.io/en/latest/best_practices/tool_xml.html](https://galaxy-iuc-standards.readthedocs.io/en/latest/best_practices/tool_xml.html).

- Always use quotes for tool directory (python3 '$__tool_directory__/psymap_simple.py') and tool parameters (--cmap '$adv.colormap')
- When wrapping an existing underlying tool, use the same version than the underlying tool
- `from_work_dir` will tell Galaxy to pick this file, this saves you the cp/mv command in the command section:

~~~`bash`
<data name="ofilename" format="png" from_work_dir="image.png"/>
~~~

- If the output format depends on the type of output file, try to avoid `auto_format` and use `change_format` instead:

~~~`bash`
<data name="ofilename" format="json">
                <change_format>
                    <when input="format" value="csv" format="csv" />
~~~               

- Add [EDAM](https://ifb-elixirfr.github.io/edam-browser) ontology in your tool, for both topics and operations. Most climate tools will have:

~~~`bash`
<edam_topics>
  <edam_topic>topic_3855</edam_topic>
  <edam_topic>topic_3318</edam_topic>
</edam_topics>
~~~               

- [Environmental science](https://ifb-elixirfr.github.io/edam-browser/#topic_3855) (topic 3855)
- [Physics](https://ifb-elixirfr.github.io/edam-browser/#topic_3318) (topic_3318)

We may need to update all the tools later when additional topics will be added for geosciences.
 

- Do not forget to follow [Galaxy IUC coding style](https://galaxy-iuc-standards.readthedocs.io/en/latest/best_practices/tool_xml.html?highlight=order#coding-style).

## Test a tool with planemo

~~~`bash`
planemo t --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~

## Serve galaxy-tools with planemo

~~~`bash`
planemo s --galaxy_root=/opt/uio/packages/galaxy --conda_prefix=/opt/uio/packages/miniconda3 mean-per-zone/mean-per-zone.xml --conda_dependency_resolution --conda_auto_install --conda_channels conda-forge,bioconda,defaults,iuc
~~~
