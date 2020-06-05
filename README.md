# MyCodeSnippets
A collection of the scripts (utility functions) that I'm using for MacOS, Linux & Windows.

## Apple Script

### 1. Sync Chrome bookmarks to Safari

An apple script that works on Safari and automatically import bookmarks from Chrome via Safari's menu bar options. Works on MacOS only. Better experience if combining the script with "cron" to automate the synchronization process. You can also import "History" and "Password" from Chrome by modifying the line 13-14 and 15-16 respectively (default only imports "Bookmarks"). e.g.

```
-- import bookmarks & History
...
key code 48 -- Tab
key code 48 -- Tab, move focus to "Password"
key code 49 -- Space, de-select "Password"
...

-- import bookmarks & Password
...
key code 48 -- Tab, move focus to "History"
key code 49 -- Space, de-select "History"
...
```

[Link to script](https://github.com/simonwu53/MyCodeSnippets/blob/master/AppleScript/sync_bookmarks.scpt)


