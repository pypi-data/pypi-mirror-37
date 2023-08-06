# TestRail cases downloader for Foliant

TestRail preprocessor collects test cases from TestRail project and adds to your testing procedure document.


## Installation

```shell
$ pip install foliantcontrib.testrail
```


## Config

To enable the preprocessor, add `testrail` to `preprocessors` section in the project config. The preprocessor has a number of options (best values are set by default where possible):

```yaml
preprocessors:
  - testrail:
    testrail_url: http://testrails.url                                  \\ Required
    testrail_login: username                                            \\ Required
    testrail_pass: password                                             \\ Required
    project_id: 35                                                      \\ Required
    suite_ids:                                                          \\ Optional
    section_ids:                                                        \\ Optional
    platforms: smarttv, androidtv, appletv, web                         \\ Optional
    platform_id: 0                                                      \\ Optional
    filename: test_cases.md                                             \\ Optional
    rewrite_src_file: true                                              \\ Optional
    template_folder: case_templates                                     \\ Optional
    section_header: Testing program                                     \\ Recommended
    std_table_header: Table with testing results                        \\ Recommended
    std_table_column_headers: №; ID; Test case name; Result; Comment    \\ Recommended
    add_cases_without_platform: true                                    \\ Optional
    add_unpublished_cases: false                                        \\ Optional
    add_case_id_to_case_name: false                                     \\ Optional
    add_std_table: true                                                 \\ Optional
    resolve_urls: true                                                  \\ Optional
    screenshots_url: https://gitlab_repository.url                      \\ Optional
    screenshots_ext: .png                                               \\ Optional
    print_case_structure: true                                          \\ For debugging
```

`testrail_url`
:   URL of TestRail deployed.

`testrail_login`
:   Your TestRail username.

`testrail_pass`
:   Your TestRail password.

`project_id`
:   TestRail project ID. You can find it in the project URL, for example http://testrails.url/index.php?/projects/overview/17 <-.

`suite_ids`
:   If you have several suites in your project, you can download test cases from certain suites. You can find suite ID in the URL again, for example http://testrails.url/index.php?/suites/view/63... <-.

`section_ids`
:   Also you can download any sections you want regardless of it's level. Just keep in mind that this setting overrides previous *suite_ids*. And suddenly you can find section ID in it's URL, for example http://testrails.url/index.php?/suites/view/124&group_by=cases:section_id&group_order=asc&group_id=3926 <-.

Now strange things, mostly made specially for my project, but may be useful for others.

You can add a custom field to your test case template in TestRail to use the same test cases for several platforms. Custom field must have system name *prj_type* and have *multi-select* type. This can be done in *Administration* panel, *Customizations* section, *Case fields* part.

`platforms`
:   List of platforms for your project. In my case it was *'smarttv, androidtv, appletv, web'* and this is value by default. You can set any platforms and but values should be the same as for *prj_type* parameter. Case insensitive.

`platform_id`
:   Platform numbers in *platforms* list. You can set any combination of platforms. Counting starts from 1. For example, in my case with *'platform_id': 1,3* will be downloaded test cases for *smarttv* and *appletv* platforms only.

That's all about platforms.

`filename`
:   Path to the test cases file. It should be added to project chapters in *foliant.yml*. Default: *test_cases.md*. For example:

```yaml
title: &title Test procedure

chapters:
    - intro.md
    - conditions.md
    - awesome_test_cases.md <- This one for test cases
    - appendum.md

preprocessors:
  - testrail:
    testrail_url: http://testrails.url
    testrail_login: username
    testrail_pass: password
    project_id: 35
    filename: awesome_test_cases.md
```

`rewrite_src_file`
:   You can update test cases file after each use of preprocessor. Be careful, previous data will be deleted.

`template_folder`
:   Preprocessor uses Jinja2 templates to compose the file with test cases. Here you can find documentation: http://jinja.pocoo.org/docs/2.10/ . You can store templates in folder inside the foliant project, but if it's not default *case_templates* you have to write it here.

If this value not set and there is no default *case_templates* folder in the project, it will be created automatically with two jinja files for TestRail templates by default — *Test Case (Text)* with *template_id=1* and *Test Case (Steps)* with *template_id=2*.

You can create TestRail templates by yourself in *Administration* panel, *Customizations* section, *Templates* part. Then you have to create jinja templates whith the names *{template_id}.j2* for them. For example, file *2.j2* for *Test Case (Steps)* TestRail template:

```

{% if case['custom_preconds'] %}
**Preconditions:**

{{ case['custom_preconds'] }}
{% endif %}

**Scenario:**

{% for case_step in case['custom_steps_separated'] %}

*Step {{ loop.index }}.* {{ case_step['content'] }}

*Expected result:*

{{ case_step['expected'] }}

{% endfor %}

```

Next three fields are necessary due localization issues. While markdown document with test cases is composed on the go, you have to set up some document headers. Definitely not the best solution in my life. 

`section_header`
:   First level header of section with test cases. By default it's *Testing program* in Russian.

`std_table_header`
:   First level header of section with test results table. By default it's *Testing table* in Russian.

`std_table_column_headers`
:   Semicolon separated headers of testing table columns. By default it's *№; ID; Test case name; Result; Comment* in Russian.

`add_cases_without_platform`
:   If you set several platforms as previously described, you still can ignore this setting and download all project test cases regardless of its platforms.

`add_unpublished_cases`
:   You can add a custom field to your test case template in TestRail to publish and unpublish test cases. Custom field must have system name *tp* (*test case publishing*) and have *checkbox* type. This can be done in *Administration* panel, *Customizations* section, *Case fields* part. With this parameter you can collect only published or all test cases.

`add_case_id_to_case_name`
:   Every test case in TestRail has unique ID, which, as usual, you can find in the header or test case URL: http://testrails.url/index.php?/cases/view/15920... <-. So you can add tis ID to test case headers and testing table. Or not.

`add_std_table`
:   You can exclude a testing table from the document.

Now about screenshots. There is no possibility to store screenshots in TestRail projects, but you can store them in the GitLab repository (link to which should be stated in one of the following parameters). GitLab project should have following structure:

```
images/
├── smarttv/
|   ├── screenshot1_smarttv.png
|   ├── screenshot2_smarttv.png
|   └── ...
├── androidtv/
|   ├── screenshot1_androidtv.png
|   ├── screenshot2_androidtv.png
|   └── ...
├── appletv/
|   ├── screenshot1_appletv.png
|   ├── screenshot2_appletv.png
|   └── ...
├── web/
|   ├── screenshot1_web.png
|   ├── screenshot2_web.png
|   └── ...
├── screenshot1.png
├── screenshot2.png
└── ...
```

*images* folder used for projects without platforms.

Now to add screenshot to your document just add following string to the test case (unfortunately, in TestRail interface it will looks like broken image link):

```
(leading exclamation mark here!)[Image title](main_filename_part)
```

Preprocessor will convert to the following format:

```
https://gitlab.url/gitlab_group_name/gitlab_project_name/raw/master/images/platform_name/main_filename_part_platform_name.png
```

For example, in project for *smarttv* platform the string

```
(leading exclamation mark here!)[Application main screen](main_screen)
```

will be converted to:

```
(leading exclamation mark here!)[Application main screen](https://gitlab.url/documentation/application-screenshots/raw/master/images/smarttv/main_screen_smarttv.png)
```

That's it.

`resolve_urls`
:   Turn on (true) or off (false, by default) image urls resolving.

`screenshots_url`
:   GitLab repository URL, in our example: https://gitlab.url/documentation/application-screenshots/ .

`screenshots_ext`
:   Screenshots extension. Yes, it must be only one and the same for all screenshots.

And the last one emergency tool. If you have no jinja template for any type of TestRail case, you'll see this message like this: *There is no jinja template for test case template_id 5 (case_id 1325) in folder case_templates*. So you have to write jinja template by yourself. To do this it's necessary to know case structure. This parameter shows it to you.

`print_case_structure`
:   Turn on (true) or off (false, by default) printing out of case structure with all data in it.


## Usage

Just add the preprocessor to the project config, set it up and enjoy the automatically collected test cases to your document.

### Tips

In some cases you may encounter a problem with test cases text format, so composed markdown file will be converted to the document with bad formatting. In this cases *replace* preprocessor could be useful: https://foliant-docs.github.io/docs/preprocessors/replace/ .
