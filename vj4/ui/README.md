# Vijos UI Framework

## Responsive Cutoffs

Vijos use the following cutoffs to determine the size of a device.

Small: `[0 - 450px)` (mobile)

Medium: `[450px, 1000px)` (tablet)

Large: `[1000px, -)` (desktop)

## Layout

### Grid

See [Foundation Grid](http://foundation.zurb.com/sites/docs/grid.html)

### Float

See [Foundation Float](http://foundation.zurb.com/sites/docs/float-classes.html)

> NOTE: `.float-center` is not implemented.

## Typography

HTML elements such as headings (`h1`, `h2`, ...), lists (`ol`, `ul`, `li`, ...) and tables does not have margins and paddings by default in order to easy the styling of semantic structures. However you may want suitable space between those elements when they are used to present content to users (for example, problem content). In this case, you need to enable the typography styling by wrapping them with `<div class="typo"></div>`:

```html
<div class="typo">
  <h1>Notice</h1>
  <p>The content will be well formatted.</p>
  <ul>
    <li>Item</li>
    <li>Item</li>
    <li>Item</li>
  </ul>
</div>
```

### Text Alignment

```html
<ANY class="text-left"></ANY>
<ANY class="text-center"></ANY>
<ANY class="text-right"></ANY>
<ANY class="text-justify"></ANY>
```

## Prototype Components

### Media Object

Media Object arranges a fixed-width media element, such as an avatar or image, beside flexible content. Use `media__left` or `media__right` for the media element and `media__body` for the content. Add `top` or `bottom` to change vertical alignment.

Example:

```html
<div class="media">
  <div class="media__left top">
    <img src="avatar.png" alt="User avatar">
  </div>
  <div class="media__body top">
    <h3>User Name</h3>
    <p>User information goes here.</p>
  </div>
</div>
```

### Number Box Object

Number Box Object displays a number with a short descriptive label. Add `large` or `medium` to `numbox__num` to control the number size.

Example:

```html
<div class="numbox">
  <div class="numbox__num large">128</div>
  <div class="numbox__text">Submissions</div>
</div>
```

### Balancer Object

Balancer Object distributes its child elements equally across a horizontal row. Each column uses `balancer__body`; add `top` or `bottom` to change its vertical alignment.

Example:

```html
<div class="balancer">
  <div class="balancer__body">
    Left content
  </div>
  <div class="balancer__body">
    Center content
  </div>
  <div class="balancer__body">
    Right content
  </div>
</div>
```

## Basic Components

### Section

Section is served as an entry to more detailed contents. By default, each section has a white background and drop-shadow.

A section should contain a section-header and one or more section bodies.

```html
<div class="section">
  <div class="section__header">
    <!-- header -->
  </div>
  <div class="section__body">
    <!-- body -->
  </div>
  <div class="section__body">
    <!-- optionally more bodies -->
  </div>
</div>
```

There will be vertical margins between section bodies.

#### Side Section

If the section is acted as a sidebar section, it should contain `side` class so that its default font size becomes smaller:

```html
<div class="section side"></div>
```

#### Title

You can use `<X class="section__title"></X>` to specify the title for a section (`X` is from `h1` to `h3`). The font size and the color of the section title is different from normal headings.

```html
<div class="section">
  <div class="section__header">
    <h1 class="section__title">Section title</h1>
  </div>
</div>
```

#### Table

If the main content of the section is a data table (or additionally with a title and a paginator), it is suggested to apply `data-table` to the table. Table should be put inside a section-body with `no-padding` decoration.

3 * 2 table sample:

```html
<div class="section">
  <!-- ... -->
  <div class="section__body no-padding">
    <table class="data-table">
      <colgroup>
        <col class="col--1">
        <col class="col--2">
      </colgroup>
      <thead>
        <tr>
          <th class="col--1"></th>
          <th class="col--2"></th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="col--1">1,1</td><td class="col--2">1,2</td></tr>
        <tr><td class="col--1">2,1</td><td class="col--2">2,2</td></tr>
        <tr><td class="col--1">3,1</td><td class="col--2">3,2</td></tr>
      </tbody>
    </table>
  </div>
</div>
```

> If you want to specify the width of a column, you should add `col--xxx` to the class name list (as shown above) and specify its width in a CSS rule like:
>
> ```css
> .col--1 { width: 120px; }
> ```

#### Samples

Section with content:

```html
<div class="section">
  <div class="section__body">
    Section content
  </div>
</div>
```

Section with title and content:

```html
<div class="section">
  <div class="section__header">
    <h1 class="section__title">Section title</h1>
  </div>
  <div class="section__body">
    Section content
  </div>
</div>
```

Section with title and table content:

```html
<div class="section">
  <div class="section__header">
    <h1 class="section__title">Section title</h1>
  </div>
  <div class="section__body no-padding">
    <table class="data-table">
      <!-- ... -->
    </table>
  </div>
</div>
```

### Button

```html
<ANY class="button"></ANY>
```

Additional class names:

`rounded`: The button would have round corners.

`primary`: The button would have blue background.

`expanded`: The button would occupy full width of the parent.

`inverse`: Removes the button background and uses a white border and white text, making it suitable for dark or immersive backgrounds.

Example:

```html
<a href="#" class="inverse rounded button">Sign Up Now</a>
```

### Input

```html
<X class="textbox"></X>
```

`X` could be `input` or `textarea` for a normal textbox.

Additional class names:

`material`: Applies the material textbox style. Add `textbox material` to a wrapping `label` and place the `input` inside it.

Example:

```html
<label class="material textbox">
  Username
  <input name="uname" type="text">
</label>
```

`inverse`: Applies light text and border colors to a material textbox for use on dark or immersive backgrounds. It must be used together with `material` on the wrapping `label`.

Example:

```html
<label class="inverse material textbox">
  Password
  <input name="password" type="password">
</label>
```

### Paginator

Paginator displays navigation links for content divided into multiple pages. Use `pager` for the list and `pager__item` for each link or indicator. Item modifiers include `first`, `previous`, `ellipsis`, `page`, `current`, `next`, and `last`; clickable items also use `link`.

Example:

```html
<ul class="pager">
  <li>
    <a class="pager__item previous link" href="?page=1">Previous</a>
  </li>
  <li>
    <a class="pager__item page link" href="?page=1">1</a>
  </li>
  <li>
    <span class="pager__item current">2</span>
  </li>
  <li>
    <a class="pager__item page link" href="?page=3">3</a>
  </li>
  <li>
    <a class="pager__item next link" href="?page=3">Next</a>
  </li>
</ul>
```

### Menu

```html
<ol class="menu">
  <li class="menu__item">
    <a href="#" class="menu__link">Item</a>
  </li>
  <li class="menu__seperator"></li>
</ol>
```

Optionally, a menu item can be `active` or `highlight` (notice that the decorator class name is added to `menu__link` instead of `menu__item`):

```html
<li class="menu__item">
  <a href="#" class="menu__link active">Active Item</a>
</li>
<li class="menu__item">
  <a href="#" class="menu__link highlight">Highlight Item</a>
</li>
```

Menu can be put inside a section. It should be placed inside `section__body no-padding` or directly inside `section`:

```html
<div class="section">
  <div>
    <ol class="menu">
    ...
    </ol>
  </div>
</div>
```

#### Menu Item from Headings

Menu items can be automatically generated from headings. To enable this feature, you need to specify the region to extract headings and the destination of extracted menu items by setting `data-heading-extract-to` attribute:

```html
<div class="section" data-heading-extract-to="#my-menu-item">
  <h1 id="h_1" data-heading>Heading 1</h1>
  <h1 id="h_2" data-heading>Heading 2</h1>
</div>
```

This attribute accepts a CSS selector and all elements that contain `data-heading` attribute in the element will be extracted. `id` is essential and it will be appended to the hash part so that the page will navigate when user clicks the newly generate menu item.

The CSS selector should match a `menu__item` element. Headings will become the sub-menu of that element.

### Sticky

Sticky elements are always visible when the user scrolls. To enable sticky, add `data-sticky` attribute to the element.

Optionally, the value of `data-sticky` can be `medium` or `large`. When `data-sticky` is `medium`, the element will be sticky only when window size is larger than mobile cutoff (can be tablet or desktop). When `data-sticky` is `large`, it will take effect only when window size is larger than desktop cutoff. See section Responsive Cutoffs for actual sizes.

The sticky element is restricted to the boundary of its closest parent. You can change this behavior by assigning attribute `data-sticky-parent` to the desired parent. `data-sticky-parent` can not be used in nested sticky elements.

A sample of sticky sidebar:

```html
<div class="row" data-sticky-parent>
  <div class="medium-9 columns">
    <!-- main content -->
  </div>
  <div class="medium-3 columns">
    <div data-sticky="large">
      <div class="section">Sticky!</div>
    </div>
  </div>
</div>
```

* Because the columns will be stacked when window size is smaller than `large` (tablet and mobile) and we don't want sidebars keep sticky in such cases, we have `data-sticky="large"` so that the element will be sticky ONLY when window size is `large`.

* The height of the two columns are not equal so the sticky parent should be `.row` instead.

### CommonMark Editor

CommonMark editor can be automatically transformed from a normal textarea. Inputs in the CommonMark editor will be synced to the textarea in real-time. To enable this feature, add `data-markdown` to the `textarea` element.

Sample:

```html
<textarea name="content" class="textbox" data-markdown></textarea>
```

> To make it work with newly added textareas, you need to trigger `vjContentNew` event for the new element. Textarea with `data-markdown` should be a children of the trigger target.

### Emoji

[Emoji code](http://www.webpagefx.com/tools/emoji-cheat-sheet/) can be automatically transformed into emoji images. To enable this feature, add `data-emoji-enabled` to the element.

Sample:

```html
<div class="typo" data-emoji-enabled></div>
```

> To make it work with newly added contents, you need to trigger `vjContentNew` event for the new element.

### Dropdown

Dropdown displays a target element when the user hovers over a trigger. Add `data-dropdown-target` to the trigger and set its value to a CSS selector identifying an element with the `dropdown-target` class. Use the optional `data-dropdown-pos` attribute to control its position; the default is `bottom left`.

Example:

```html
<div data-dropdown-target="#example-menu" data-dropdown-pos="bottom right">
  <button class="button">Open Menu</button>

  <ol class="dropdown-target menu" id="example-menu">
    <li class="menu__item">
      <a class="menu__link" href="#">Profile</a>
    </li>
    <li class="menu__item">
      <a class="menu__link" href="#">Settings</a>
    </li>
  </ol>
</div>
```

The framework creates the external dropdown wrapper automatically, so `dropdown` and `drop-content` normally do not need to be added manually.

### Navigation

Navigation provides the primary responsive navigation structure. Use `nav__list--main` for the main links, `nav__list--secondary` for links aligned on the opposite side, and `nav--active` on the active `nav__item`.

Example:

```html
<nav class="nav slideout-menu" id="menu">
  <div class="row">
    <div class="columns clearfix">
      <ol class="nav__list nav__list--main clearfix">
        <li class="nav__list-item">
          <a class="nav__item nav--active" href="#">Home</a>
        </li>
        <li class="nav__list-item">
          <a class="nav__item" href="#">Problems</a>
        </li>
      </ol>

      <ol class="nav__list nav__list--secondary clearfix">
        <li class="nav__list-item">
          <a class="nav__item--round" href="#">Sign Up</a>
        </li>
      </ol>
    </div>
  </div>
</nav>
```

### Star

Star provides an interactive control for starring and unstarring an item. Place the button inside a form containing an input named `operation`. The component changes the operation between `star` and `unstar`, submits the form asynchronously, and toggles the `activated` class.

Use `starred--hide` for content shown when the item is not starred and `starred--show` for content shown when it is starred. Add `activated` to the button and use `unstar` as the initial operation when the item is initially starred.

Example:

```html
<form action="/star" method="post">
  <input type="hidden" name="operation" value="star">

  <button class="star" type="submit">
    <span class="starred--hide">
      <span class="icon icon-star--outline"></span>
      Star
    </span>
    <span class="starred--show">
      <span class="icon icon-star"></span>
      Unstar
    </span>
  </button>
</form>
```

### Tab

Tab organizes related content into switchable panels. Place `section__tabs` inside `section__tab-container`. Each `section__tab-item` must contain a `section__tab-title` and its corresponding `section__tab-main`.

When JavaScript is enabled, the framework generates the clickable tab headers and content wrappers automatically. Without JavaScript, each tab remains visible as a normal section.

Example:

```html
<div class="section__tab-container immersive">
  <ul class="section__tabs">
    <li class="section__tab-item">
      <h1 class="section__tab-title">Overview</h1>
      <div class="section__tab-main">
        Overview content.
      </div>
    </li>

    <li class="section__tab-item">
      <h1 class="section__tab-title">Submissions</h1>
      <div class="section__tab-main">
        Submission content.
      </div>
    </li>
  </ul>
</div>
```

### Hotkey

#### Local Hotkey

Local hotkeys are triggered when it is assigned to a parent of the active element in which user presses specific key.

To enable local hotkey on an element, add `data-hotkey` attribute:

```html
<button data-hotkey="f1"></button>
```

You can specify multiple hotkeys in the attribute.

#### Global hotkey

Global hotkeys are triggered no matter where user presses specific key.

To enable global hotkey on an element, add `data-global-hotkey` attribute:

```html
<button data-global-hotkey="f2"></button>
```

You can specify multiple hotkeys in the attribute.

#### Hotkey Syntax

`hotKeyDef[,hotKeyDef[,hotKeyDef...]]`

`hotKeyDef`: `keySequence[:event]`

`keySequence`: `key1[+key2[+key3...]]`

When `keySequence` matches, the `event` will be triggered on the element that holds the attribute. If `event` is not given in `hotKeyDef`, it will be `click` by default. In addition, if `event` is `submit`, the event will be triggered on the closest `form` element, instead of the current element.

Sample:

`ctrl+f1`: Triggers click on this element when user presses `Ctrl`+`F1` or `Command`+`F1`.

`ctrl+enter:submit`: Triggers submit on the closest `form` when user presses `Ctrl+Enter` or `Command+Enter`.

`f1:submit,f2:client`: Triggers submit when user presses `f1` and triggers click when user presses `f2`.

### Tooltip

```html
<X data-tooltip="your tooltip text"></X>
```

Optionally, you can specify a location by assigning `data-tooltip-pos` attribute. Available values are:

* `"top left"`
* `"top middle"` (default)
* `"top right"`
* `"bottom left"`
* `"bottom middle"`
* `"bottom right"`

## High-Level Components

### Comment List

Comment List displays comments and nested replies using the Media Object layout. The outer list uses `dczcomments__list`, top-level comments use `dczcomments__item`, and nested replies use `dczcomments__reply` inside `dczcomments__replies`.

Use `dczcomments__supplementary` for author and time information and `dczcomments__operations` for actions such as reply, edit, or delete.

Example:

```html
<ul class="dczcomments__list view--discussion">
  <li class="dczcomments__item">
    <div class="media">
      <div class="media__left top">
        <img src="avatar.png" alt="User avatar" width="60" height="60">
      </div>

      <div class="media__body top no-heading">
        <div class="clearfix">
          <div class="supplementary dczcomments__supplementary">
            User Name @ 5 minutes ago
          </div>
          <div class="dczcomments__operations">
            <a href="#">Reply</a>
          </div>
        </div>

        <div class="typo">
          Comment content.
        </div>

        <ul class="dczcomments__replies">
          <li class="dczcomments__reply">
            <div class="media">
              <div class="media__body top no-heading">
                Reply content.
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </li>
</ul>
```

## Other

### JavaScript-Responsive Visibility

#### Hide if JavaScript is disabled

```html
<ANY class="nojs--hide"></ANY>
```

#### Hide if JavaScript is enabled

```html
<ANY class="hasjs--hide"></ANY>
```
