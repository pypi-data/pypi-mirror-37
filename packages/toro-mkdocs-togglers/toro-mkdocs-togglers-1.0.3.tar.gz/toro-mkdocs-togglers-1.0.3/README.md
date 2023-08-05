## TORO Toggler Markdown Extension

Content Toggler Markdown extension for TORO Documentation.


#### Installation
```
pip install toro-mkdocs-togglers
```

#### Usage

To properly use the toggler extension use the following markdown:
```
||| "TabName1"
    Tab1 content.
||| "TabName2"
    Tab2 content.
```

The produced HTML from the markdown will be:
```
<div class="toro-toggler" data-names="TabName1,TabName2">
    <div data-related-divider="TabName1">
        <p>Tab1 content.</p>
    </div>
    <div data-related-divider="TabName2">
        <p>Tab2 content.</p>
    </div>
</div>
```

To use the toggler extension with a nested toggler use the following markdown:
```
||| "TabName1"
    /// "NestedTabName1"
        Nested Tab1 content.
    /// "NestedTabName2"
        Nested Tab2 content.
||| "TabName2"
    Tab2 content.
```

The produced HTML from the markdown will be:
```
<div class="toro-toggler" data-names="TabName1,TabName2">
    <div data-related-divider="TabName1">
        <div class="toro-toggler" data-names="NestedTabName1,NestedTabName2">
            <div data-related-divider="NestedTabName1">
                <p>Nested Tab1 content.</p>
            </div>
            <div data-related-divider="NestedTabName2">
                <p>Nested Tab2 content.</p>
            </div>
        </div>
    </div>
    <div data-related-divider="TabName2">
        <p>Tab2 content.</p>
    </div>
</div>
```