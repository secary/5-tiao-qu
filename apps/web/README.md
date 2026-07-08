# Web

Next.js + TypeScript 网页端，MVP 首屏直接进入三栏规则查询工作台。

## 本地启动

```powershell
npm install
npm run dev:web
```

默认访问 `http://localhost:3000`。接口地址通过根目录 `.env` 中的 `NEXT_PUBLIC_API_BASE_URL` 配置。

## 目录约定

- `src/app`：Next.js App Router 页面和全局样式。
- `src/app/page.tsx`：MVP 工作台入口，后续接入真实上传、查询和引用数据。
- `@5-tiao-qu/shared`：前后端共享的回答类型、导入状态和引用结构。
