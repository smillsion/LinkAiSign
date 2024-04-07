# LinkAiSign
[![Last Commit](https://img.shields.io/github/last-commit/smillsion/LinkAiSign.svg?color=blue&label=%E6%9C%80%E8%BF%91%E6%8F%90%E4%BA%A4)](https://github.com/smillsion/LinkAiSign/commits/main)

link-ai签到获取积分

## 更新
2024-04-07 增加账号密码登陆（需要绑定手机号）

2024-04-03 增加bark失败推送

2024-04-02 返回用户积分总计

## 功能
1. 签到获取积分和返回总积分
2. 自动更新token（需配置账户名和密码）

## 拉库指令
青龙拉库指令 `ql repo https://smillsion/LinkAiSign.git`

## 环境变量
### 1.`LinkAiToken`
* 方式一（微信扫码登陆，token有效期为7天）：
  * 登陆[Link-Ai平台](https://link-ai.tech/home)后在浏览器控制台执行以下代码
    ``` javascript
    console.log(localStorage.token);
    ```
  * 将以上获得的密钥，添加到环境变量 `LinkAiToken` 后即可使用
* 方式二（需要绑定手机号，通过账号密码登陆自动获取）：
  * 手动增加环境变量`LA_USERNAME`和`LA_PASSWORD`
  * 执行脚本后会自动添加 `LinkAiToken`环境变量
  * **注：采用方式二，签到时检测到Token过期会尝试使用账号密码登陆获取新的token写入环境变量，如果不是自建的青龙，强烈不建议采用本方式，本人不对采用该方式导致的任何损失负责**
  
### 2. 失败推送（目前只支持IOS设备）
* **bark推送**，配置 `MT_BARK_SERVER` 和 `MT_BARK_KEY` 环境变量
* bark介绍及用法，跳转[【bark】](https://github.com/Finb/Bark)

## 贡献代码
项目没有经过严格测试。有问题可以在 **[Issues](https://github.com/smillsion/LinkAiSign/issues)** 反馈。

若您有好的想法，发现一些 **BUG** 并修复了，欢迎提交 **[Pull Request](https://github.com/smillsion/LinkAiSign/pulls)** 参与开源贡献。

## 声明
本仓库内容仅做个人学习用途，我不会对因为滥用该项目导致的任何问题负责。