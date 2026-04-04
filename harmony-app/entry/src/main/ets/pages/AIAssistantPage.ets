// QuantAI HarmonyOS NEXT - AI 助手页
// ArkTS + ArkUI

const COLOR_BG = '#0A1628';
const COLOR_CARD = '#111F35';
const COLOR_GREEN = '#00C896';
const COLOR_TEXT = '#E8F4FF';
const COLOR_MUTED = '#6B8DB0';
const COLOR_BORDER = '#1E3050';
const COLOR_USER_BUBBLE = '#1E3050';
const COLOR_AI_BUBBLE = '#0D2340';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  time: string;
}

@Component
export struct AIAssistantPage {
  @State messages: ChatMessage[] = [
    {
      role: 'assistant',
      content: '你好！我是 QuantAI 智能助手 🤖\n\n我可以帮你：\n• 分析市场行情\n• 策略建议\n• 帮你下单交易\n• 风险管理建议\n\n请直接告诉我你想做什么！',
      time: '09:00'
    }
  ];
  @State inputText: string = '';
  @State isLoading: boolean = false;
  private listScroller: Scroller = new Scroller();

  private quickReplies: string[] = ['分析BTC行情', '做多ETH', '查看我的持仓', '市场风险评估'];

  private getAIReply(msg: string): string {
    const lower = msg.toLowerCase();
    if (lower.includes('btc') || lower.includes('比特币')) {
      return '📊 BTC/USDT 技术分析：\n\n• 当前价格：$83,250\n• 趋势：短期上升通道\n• RSI：58（偏多但未超买）\n• MACD：金叉确认\n\n💡 建议：可轻仓做多，止损设 $81,500，目标 $86,000。';
    } else if (lower.includes('eth') || lower.includes('以太')) {
      return '📈 ETH/USDT 技术分析：\n\n• 当前价格：$1,842\n• 趋势：横盘整理\n• 支撑位：$1,800\n• 阻力位：$1,900\n\n💡 建议：等待有效突破 $1,900 后入场。';
    } else if (lower.includes('做多') || lower.includes('买入')) {
      return '⚡ 收到下单指令！\n\n请确认订单详情：\n• 方向：做多（买入）\n• 品种：BTC/USDT\n• 数量：0.1 BTC\n• 杠杆：10x\n• 预计保证金：$83.25\n\n点击下方"确认下单"按钮执行。';
    } else if (lower.includes('持仓') || lower.includes('仓位')) {
      return '📊 您当前持仓：\n\n1. BTC/USDT 做多 0.1\n   入场：$82,800 | 当前：$83,250\n   盈亏：+$45 (+0.54%)\n\n2. ETH/USDT 做多 1.0\n   入场：$1,858 | 当前：$1,842\n   盈亏：-$16 (-0.86%)\n\n总浮盈：+$29 (+0.12%)';
    } else if (lower.includes('风险') || lower.includes('risk')) {
      return '🛡️ 风险评估报告：\n\n• 仓位利用率：42%（正常）\n• 今日最大回撤：1.8%（安全）\n• 杠杆比例：8x（建议≤10x）\n• 风险等级：⭐⭐（中低风险）\n\n建议：当前配置合理，注意控制单仓不超过总资金10%。';
    } else {
      return '收到！我正在分析您的请求...\n\n您可以尝试：\n• 「分析 BTC/ETH 行情」\n• 「做多/做空 BTC 0.1」\n• 「查看持仓详情」\n• 「给我风险建议」';
    }
  }

  sendMessage() {
    if (!this.inputText.trim() || this.isLoading) return;
    const userMsg = this.inputText.trim();
    const now = new Date();
    const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;

    this.messages.push({ role: 'user', content: userMsg, time: timeStr });
    this.inputText = '';
    this.isLoading = true;

    // 模拟 AI 延迟响应
    setTimeout(() => {
      const reply = this.getAIReply(userMsg);
      this.messages.push({ role: 'assistant', content: reply, time: timeStr });
      this.isLoading = false;
      // 滚到底部
      this.listScroller.scrollEdge(Edge.Bottom);
    }, 800);
  }

  @Builder
  MessageBubble(msg: ChatMessage) {
    Row() {
      if (msg.role === 'assistant') {
        // AI 头像
        Text('🤖')
          .fontSize(20)
          .margin({ right: 8 })
          .alignSelf(ItemAlign.Start)
          .margin({ top: 4 })
      }

      Column({ space: 4 }) {
        Text(msg.content)
          .fontSize(13)
          .fontColor(COLOR_TEXT)
          .lineHeight(20)
          .backgroundColor(msg.role === 'assistant' ? COLOR_AI_BUBBLE : COLOR_USER_BUBBLE)
          .padding(12)
          .borderRadius(12)
          .maxLines(100)
        Text(msg.time)
          .fontSize(10)
          .fontColor(COLOR_MUTED)
          .alignSelf(msg.role === 'user' ? ItemAlign.End : ItemAlign.Start)
      }
      .layoutWeight(1)

      if (msg.role === 'user') {
        Text('👤')
          .fontSize(20)
          .margin({ left: 8 })
          .alignSelf(ItemAlign.Start)
          .margin({ top: 4 })
      }
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .direction(msg.role === 'user' ? Direction.Rtl : Direction.Ltr)
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('🤖 AI 智能助手')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor(COLOR_TEXT)
        Blank()
        Text('历史')
          .fontSize(13)
          .fontColor(COLOR_MUTED)
      }
      .width('100%')
      .padding({ top: 16, left: 16, right: 16, bottom: 8 })

      // 消息列表
      List({ scroller: this.listScroller }) {
        ForEach(this.messages, (msg: ChatMessage, index: number) => {
          ListItem() {
            this.MessageBubble(msg)
          }
        })
        if (this.isLoading) {
          ListItem() {
            Row() {
              Text('🤖').fontSize(20).margin({ right: 8 })
              Text('AI 正在思考...')
                .fontSize(13)
                .fontColor(COLOR_MUTED)
                .backgroundColor(COLOR_AI_BUBBLE)
                .padding(12)
                .borderRadius(12)
            }
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          }
        }
      }
      .layoutWeight(1)
      .width('100%')

      // 快速回复
      Scroll() {
        Row({ space: 8 }) {
          ForEach(this.quickReplies, (reply: string) => {
            Text(reply)
              .fontSize(12)
              .fontColor(COLOR_GREEN)
              .backgroundColor(COLOR_CARD)
              .padding({ top: 6, bottom: 6, left: 12, right: 12 })
              .borderRadius(16)
              .border({ width: 1, color: COLOR_GREEN + '60' })
              .onClick(() => {
                this.inputText = reply;
                this.sendMessage();
              })
          })
        }
        .padding({ left: 16, right: 16 })
      }
      .scrollable(ScrollDirection.Horizontal)
      .scrollBar(BarState.Off)
      .height(44)
      .margin({ bottom: 8 })

      // 输入栏
      Row({ space: 8 }) {
        TextInput({ placeholder: '发消息给 AI 助手...', text: this.inputText })
          .layoutWeight(1)
          .height(44)
          .backgroundColor(COLOR_CARD)
          .fontColor(COLOR_TEXT)
          .placeholderColor(COLOR_MUTED)
          .borderRadius(22)
          .padding({ left: 16, right: 16 })
          .border({ width: 1, color: COLOR_BORDER })
          .onChange((val) => { this.inputText = val; })
          .onSubmit(() => this.sendMessage())

        Button('发送')
          .height(44)
          .width(70)
          .backgroundColor(COLOR_GREEN)
          .fontColor('#0A1628')
          .fontWeight(FontWeight.Bold)
          .fontSize(14)
          .borderRadius(22)
          .onClick(() => this.sendMessage())
      }
      .padding({ left: 16, right: 16, bottom: 16 })
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor(COLOR_BG)
  }
}
