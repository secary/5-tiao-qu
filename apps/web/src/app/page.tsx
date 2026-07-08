import { BookOpen, FileText, Send, Upload } from "lucide-react";
import type {
  AnswerType,
  Citation,
  ImportStatus,
  SourceType
} from "@5-tiao-qu/shared";

const rulebooks: Array<{
  id: string;
  title: string;
  game: string;
  status: ImportStatus;
  progress: number;
}> = [
  {
    id: "ark-nova",
    title: "规则书 v1.0",
    game: "示例桌游",
    status: "ready",
    progress: 100
  }
];

const answer: {
  type: AnswerType;
  conclusion: string;
  detail: string;
} = {
  type: "direct_rule",
  conclusion: "结论：当前示例答案有直接引用支撑。",
  detail:
    "正式接入检索前，后端会在没有命中规则片段时返回“规则书中未找到明确说明”，避免无依据裁定。"
};

const citations: Citation[] = [
  {
    id: "cite-1",
    chunkId: "chunk-12",
    pageNumber: 7,
    chapterTitle: "移动与阻挡",
    chunkText:
      "角色移动时，需要按照规则书列出的阻挡条件判断路径是否可通过。",
    sourceFile: "sample-rulebook.pdf",
    sourceType: "base_rulebook" satisfies SourceType,
    sourcePriority: 100,
    similarityScore: 0.82
  }
];

export default function Home() {
  return (
    <main className="workspace">
      <aside className="sidebar" aria-label="规则书">
        <div className="brand">
          <BookOpen aria-hidden="true" size={22} />
          <div>
            <h1>5 条区</h1>
            <p>规则查询工作台</p>
          </div>
        </div>

        <button className="uploadButton" type="button">
          <Upload aria-hidden="true" size={18} />
          上传规则书
        </button>

        <section className="stack" aria-label="已导入规则书">
          {rulebooks.map((rulebook) => (
            <article className="rulebookItem" key={rulebook.id}>
              <div className="itemTitle">
                <FileText aria-hidden="true" size={18} />
                <div>
                  <h2>{rulebook.game}</h2>
                  <p>{rulebook.title}</p>
                </div>
              </div>
              <div className="progressTrack" aria-label="导入进度">
                <span style={{ width: `${rulebook.progress}%` }} />
              </div>
              <div className="statusLine">
                <span>{statusLabel[rulebook.status]}</span>
                <strong>{rulebook.progress}%</strong>
              </div>
            </article>
          ))}
        </section>
      </aside>

      <section className="chatPanel" aria-label="规则问答">
        <header className="chatHeader">
          <div>
            <p className="eyebrow">当前规则书</p>
            <h2>示例桌游 · 规则书 v1.0</h2>
          </div>
          <span className={`answerType ${answer.type}`}>直接依据</span>
        </header>

        <div className="messages">
          <article className="message question">
            <p>攻击时可以穿过队友吗？</p>
          </article>
          <article className="message response">
            <p className="conclusion">{answer.conclusion}</p>
            <p>{answer.detail}</p>
            <div className="inlineCitations">
              {citations.map((citation) => (
                <a href={`#${citation.id}`} key={citation.id}>
                  第 {citation.pageNumber} 页
                </a>
              ))}
            </div>
          </article>
        </div>

        <form className="askBox">
          <input
            aria-label="输入规则问题"
            placeholder="输入规则问题..."
            type="text"
          />
          <button type="button" aria-label="发送问题">
            <Send aria-hidden="true" size={18} />
          </button>
        </form>
      </section>

      <aside className="citationPanel" aria-label="引用来源">
        <header>
          <p className="eyebrow">引用来源</p>
          <h2>可追溯依据</h2>
        </header>

        <div className="citationList">
          {citations.map((citation) => (
            <article className="citationItem" id={citation.id} key={citation.id}>
              <div className="citationMeta">
                <strong>第 {citation.pageNumber} 页</strong>
                <span>{citation.chapterTitle}</span>
              </div>
              <p>{citation.chunkText}</p>
              <dl>
                <div>
                  <dt>来源</dt>
                  <dd>{citation.sourceFile}</dd>
                </div>
                <div>
                  <dt>优先级</dt>
                  <dd>{citation.sourcePriority}</dd>
                </div>
                <div>
                  <dt>相似度</dt>
                  <dd>{citation.similarityScore?.toFixed(2)}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>

        <div className="pagePreview" aria-label="页面预览">
          <span>PDF 页面预览</span>
        </div>
      </aside>
    </main>
  );
}

const statusLabel: Record<ImportStatus, string> = {
  uploaded: "已上传",
  extracting: "解析中",
  chunking: "切分中",
  embedding: "索引中",
  ready: "可查询",
  failed: "导入失败"
};
