## 插件简介
这个插件是用于连接[cow](https://github.com/zhayujie/chatgpt-on-wechat)项目到[coze](https://www.coze.com/)服务，通过[coze-discord-proxy](https://github.com/deanxv/coze-discord-proxy?tab=readme-ov-file)，以免费获得ChatGPT-4.0和DALL·E 3的功能。

## 安装和配置步骤
1. **安装Git**
   - 安装命令：
     ```
     sudo yum install git -y
     ```
   - 进入插件文件夹：
     ```
     cd /home/wechat/chatgpt-on-wechat/plugins/   # 使用实际路径
     ```
   - 克隆仓库到`plugins` 文件夹：
     ```
     git clone https://github.com/MasterKeee/coze.git
     ```

2. **配置插件**
   - 进入`coze` 文件夹，找到 `config.json.template` 文件，复制并重命名为 `config.json`：
     ```
     cp config.json.template config.json
     ```
   - 编辑 `config.json`
        ```
        vi config.json
        ```
      填入相应内容：

     ```json
     {
       "apiKey": "xxxxx",  // 在coze-discord-proxy的docker-compose.yml中找到PROXY_SECRET
       "apiUrl": "xxxxx/v1/chat/completions",  // 在coze-discord-proxy的docker-compose.yml中找到PROXY_URL
       "channelId": "xxxxx",  // 在coze-discord-proxy的docker-compose.yml中找到CHANNEL_ID
       "createImgPrefix":"画"   //画图前缀
     }
     ```
   - 保存并退出编辑器：按 `Esc` 键，输入 `:wq`。

3. **配置cow `config.json`**
   - 返回插件根目录并编辑：
     ```
     cd /home/wechat/chatgpt-on-wechat   # 使用实际路径
     vi config.json
     ```
   - 找到并修改 `"image_create_prefix": ["画"]` 为其他与本插件画图前缀不同的内容。

4. **运行项目**
   - 启动项目：
     ```
     nohup python3 app.py & tail -f nohup.out
     ```

## 使用方法
- 发送命令如“画一个太阳”，即可触发DALL·E 3插件生成图片。

## 额外说明
- 已有[coze-discord-proxy](https://github.com/deanxv/coze-discord-proxy?tab=readme-ov-file)配置。
- 需要复制并修改 config.json.template 文件，填入相关参数。
- 若要避免冲突，需修改cow项目根目录下的 config.json 文件中画图前缀(image_create_prefix)。
- 使用#reloadp命令可扫描并加载新插件。

## 交流群
- **Telegram 交流群**：[加入群组](https://t.me/ggkejishuo_group)
- **微信公众号**：`基基科技说` 可查看插件效果。
- **QQ 交流群**：[加入群组](https://qm.qq.com/cgi-bin/qm/qr?k=mZ1hKsGn4Y)

请按以上步骤操作，如有疑问，随时提问。