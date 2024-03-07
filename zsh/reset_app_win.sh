#!/bin/zsh

# 输入应用名称
echo "请输入应用程序的名称（如：Safari）："
read appName

# 获取输入的 bundle identifier
bundleId=$(osascript -e "id of app \"$appName\"")

# 检查 bundle identifier 是否获取成功
if [ -z "$bundleId" ]; then
    echo "无法获取应用的 bundle identifier。"
    exit 1
fi

echo "应用的 bundle identifier 是：$bundleId"

# 查找窗口位置信息
# 尝试在两个可能的位置查找 plist 文件
plistPaths=("$HOME/Library/Containers/$bundleId/Data/Library/Preferences/$bundleId.plist" "$HOME/Library/Preferences/$bundleId.plist")
foundPlist=""

for plistPath in "${plistPaths[@]}"; do
    if [ -f "$plistPath" ]; then
        echo "找到 plist 文件：$plistPath"
        foundPlist=$plistPath
        break
    fi
done

if [ -z "$foundPlist" ]; then
    echo "未找到 plist 文件。"
    exit 1
fi

# 使用 plutil 和 grep 查找窗口位置信息
windowFrames=$(plutil -p "$foundPlist" | grep NSWindow | grep Frame)

if [ -z "$windowFrames" ]; then
    echo "未找到窗口位置信息。"
    exit 1
fi

echo "找到的窗口位置信息如下："
echo "$windowFrames"

# 选择要删除的窗口信息字段
echo "请输入您想要删除的窗口信息字段（例如：NSWindow Frame MainWindow）："
read frameKey

# 删除选中的字段
defaults delete "$bundleId" "$frameKey"

echo "已删除指定的窗口位置信息。"
