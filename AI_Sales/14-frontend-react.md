# Chapter 14: Frontend A, React

> 🎯 **What you will learn**
> - What React, TypeScript and Vite are, in plain words
> - How to run the React screen against the **mock backend** (no cloud)
> - The four React ideas that explain the whole app: component, props, state, effect
> - Every file in `frontend-react/src`, what it does and why
> - How the build-time setting `VITE_API_BASE_URL` works (and why it surprises beginners)
> - How to build a production image

⏱️ Time: about 2 hours. You do **not** need to know React. If you prefer pure Python, [Chapter 15](15-frontend-streamlit.md) builds the same screen with Streamlit.

---

## 🧸 The Lego analogy

A React screen is built from **Lego bricks** called *components*. A small brick (a drop-down) snaps into a bigger one (the selector row), which snaps into a page, which snaps into the app. Each brick:

- gets its **settings** from the brick above (*props*),
- remembers its **own little notes** (*state*),
- and when the notes change, React redraws **only that brick**.

| Word | Plain meaning |
|---|---|
| **React** | A library for building screens from components |
| **TypeScript** | JavaScript with *labels on values* (`productId: string`), so mistakes show up before you run the app |
| **Vite** | The tool that runs a fast dev server and builds the final files |
| **Component** | A function that returns a piece of screen (written in JSX, which looks like HTML) |
| **Props** | Inputs to a component, like function arguments |
| **State** | A value the component remembers; changing it redraws the component |
| **Effect** (`useEffect`) | "Do this after the screen is drawn", for example fetch data |
| **Hook** | A function whose name starts with `use` and gives a component a feature (`useState`, `useEffect`, our own `useCountUp`) |
| **axios** | A library that sends HTTP requests |
| **recharts** | A chart library |

---

## ▶️ Run it (no cloud needed)

You need **Node.js 22** (see [Chapter 3](03-setup-and-costs.md)).

**Terminal 1: mock backend** (from the repository root)

```bash
pip install fastapi uvicorn pandas python-multipart
python tools/mock_backend.py
```

**Terminal 2: React**

```bash
cd frontend-react
cp .env.example .env        # Windows PowerShell: copy .env.example .env
npm install
npm run dev
```

Open **<http://localhost:5173>**.

![React dashboard](../images/screenshots/ch14-react-dashboard.png)

> 🧪 To use the real backend, start it as in [Chapter 3](03-setup-and-costs.md). Only `VITE_API_BASE_URL` in `.env` decides which one you talk to.

Useful commands:

| Command | Meaning |
|---|---|
| `npm install` | Download the packages listed in `package.json` |
| `npm run dev` | Dev server with instant reload |
| `npm run build` | Type-check (`tsc -b`) and build the production files into `dist/` |
| `npm run lint` | Check code style with oxlint |
| `npm run preview` | Serve the built files locally |

---

## 🗺️ The component tree

![Component tree](../images/diagrams/ch14-01-component-tree.svg)

```text
frontend-react/
├── package.json            ← packages and commands
├── vite.config.ts          ← tiny: just enables the React plugin
├── .env.example            ← VITE_API_BASE_URL
├── Dockerfile              ← build with Node, serve with Nginx
├── index.html              ← one empty <div id="root">
└── src/
    ├── main.tsx            ← starts React
    ├── App.tsx             ← routes (2 pages)
    ├── api/                ← all backend calls
    │   ├── client.ts       ← one shared axios object
    │   ├── types.ts        ← the shape of every JSON answer
    │   ├── forecast.ts
    │   ├── chat.ts
    │   └── pipeline.ts
    ├── components/         ← the Lego bricks
    ├── hooks/useCountUp.ts ← count-up animation
    ├── pages/              ← DashboardPage, AnalyticsChatPage
    ├── App.css, index.css  ← styles
    └── assets/
```

> 🧱 **Same design rule as the backend:** *screens never build URLs.* Components call a function from `src/api/`, and `src/api/` deals with HTTP.

---

## 🔄 From a click to the backend

![Data flow](../images/diagrams/ch14-02-data-flow.svg)

Every box in the left column is a component. Every box in the middle is a function in `src/api/`. All of them share **one** axios client (`client.ts`), and each ends at one FastAPI endpoint from [Chapter 12](12-backend-fastapi.md).

---

## 📖 Walkthrough, file by file

### 1. `main.tsx` and `App.tsx`: start and routes

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

`createRoot(...).render(<App />)` finds the empty `<div id="root">` in `index.html` and draws the app inside it. `StrictMode` is a development helper that warns about risky code.

```tsx
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import AnalyticsChatPage from './pages/AnalyticsChatPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/analytics" element={<AnalyticsChatPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

`BrowserRouter` and `Routes` give the app **two pages** without reloading the browser: `/` (Dashboard) and `/analytics` (Chat). `Layout` wraps both, so the top bar is written once.

```tsx
import { NavLink, Outlet } from 'react-router-dom'

function navLinkClass({ isActive }: { isActive: boolean }) {
  return isActive ? 'nav-link nav-link--active' : 'nav-link'
}

function Layout() {
  return (
    <div className="app-shell">
      <nav className="topbar">
        <div className="brand">
          <span className="brand-mark">Sales AI</span>
        </div>
        <div className="nav-links">
          <NavLink to="/" end className={navLinkClass}>
            Dashboard
          </NavLink>
          <NavLink to="/analytics" className={navLinkClass}>
            Analytics Chat
          </NavLink>
        </div>
      </nav>
      <Outlet />
    </div>
  )
}

export default Layout
```

`NavLink` is a link that knows when it is the current page (`isActive`), so we can highlight it. `<Outlet />` is the hole where the chosen page appears.

### 2. `api/client.ts`: one shared axios object

```ts
import axios from 'axios'

// Configured from VITE_API_BASE_URL so the target backend can be swapped per
// environment (local dev, docker-compose, deployed) without a code change.
// See .env.example for the expected variable name.
const baseURL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const apiClient = axios.create({
  baseURL,
  timeout: 10000,
})

export default apiClient
```

- `import.meta.env.VITE_API_BASE_URL` is where Vite puts values from `.env`. Only names starting with `VITE_` are exposed.
- `?? 'http://localhost:8000'` is the default if the variable is missing.
- `timeout: 10000` means give up after 10 seconds. Slow calls override this (below).

### 3. `api/forecast.ts` and `api/chat.ts`

```ts
import apiClient from './client'
import type { ForecastExplanation, ForecastHistoryResponse, Product, Store } from './types'

export async function getProducts(): Promise<Product[]> {
  // Opens its own Databricks connection server-side (a few seconds of
  // overhead on its own); give it more room than the client's 10s default.
  const { data } = await apiClient.get<Product[]>('/products', { timeout: 20000 })
  return data
}

export async function getStores(): Promise<Store[]> {
  const { data } = await apiClient.get<Store[]>('/stores', { timeout: 20000 })
  return data
}

export async function getForecastWithHistory(
  productId: string,
  storeId: string,
  historyDays = 90,
): Promise<ForecastHistoryResponse> {
  const { data } = await apiClient.get<ForecastHistoryResponse>('/forecast', {
    params: {
      product_id: productId,
      store_id: storeId,
      include_history: true,
      history_days: historyDays,
    },
  })
  return data
}

export async function explainForecast(
  productId: string,
  storeId: string,
  userQuestion?: string,
): Promise<ForecastExplanation> {
  // Multiple Databricks queries plus an LLM call routinely take well over the
  // client's default 10s timeout -- give this one significantly more room.
  const { data } = await apiClient.post<ForecastExplanation>(
    '/forecast/explain',
    {
      product_id: productId,
      store_id: storeId,
      user_question: userQuestion,
    },
    { timeout: 60000 },
  )
  return data
}
```

Each function is `async` (it waits for the network) and returns a **typed** promise, for example `Promise<Product[]>`. The comments explain why some calls get a longer timeout: *explain* runs several Databricks queries plus an AI call, so it gets 60 seconds.

```ts
import apiClient from './client'
import type { ChatResponse, ChatTurnHistory, KPISummary } from './types'

// Both the free-text and quick-action calls hit the LLM tool-calling path
// (or, for quick actions, compute over real data without an LLM) and can
// take a while -- give them the same generous timeout as /forecast/explain.
const CHAT_TIMEOUT_MS = 60000

export async function sendChatMessage(
  message: string,
  history: ChatTurnHistory[] = [],
  storeId?: string,
  storeName?: string,
): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>(
    '/chat',
    { message, history, store_id: storeId || null, store_name: storeName || null },
    { timeout: CHAT_TIMEOUT_MS },
  )
  return data
}

export async function sendQuickAction(
  action: string,
  params: Record<string, unknown> = {},
): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>(
    '/chat/quick',
    { action, params },
    { timeout: CHAT_TIMEOUT_MS },
  )
  return data
}

export async function getKPIs(): Promise<KPISummary> {
  // /kpis runs 5 aggregate queries server-side; comfortably under the
  // default 10s client timeout in normal operation, but a cold/slow
  // Databricks warehouse can still exceed it, so give it extra room.
  const { data } = await apiClient.get<KPISummary>('/kpis', { timeout: 30000 })
  return data
}
```

`store_id: storeId || null` turns an empty string into `null`, which the backend expects for "no store".

### 4. `api/pipeline.ts`: uploads and status

```ts
import apiClient from './client'
import type {
  PipelineStatusResponse,
  PipelineTriggerResponse,
  PipelineUploadAndTriggerResponse,
  PipelineUploadResponse,
} from './types'

// Uploads (and the job trigger itself) can take a few seconds longer than
// the client's default 10s timeout -- same reasoning as the chat/explain
// endpoints elsewhere in this app.
const PIPELINE_TIMEOUT_MS = 60000

// The backend has two NAMED form fields (not a generic "files" list), so the
// field is chosen from the start of the file name. At most one file per field.
function buildUploadFormData(files: File[]): FormData {
  const formData = new FormData()
  files.forEach((file) => {
    const field = file.name.startsWith('calendar_marketing_external')
      ? 'calendar_marketing_file'
      : 'sales_transactions_file'
    formData.append(field, file)
  })
  return formData
}

export async function uploadPipelineFiles(files: File[]): Promise<PipelineUploadResponse> {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))
  const { data } = await apiClient.post<PipelineUploadResponse>('/pipeline/upload', formData, {
    timeout: PIPELINE_TIMEOUT_MS,
  })
  return data
}

export async function triggerPipeline(): Promise<PipelineTriggerResponse> {
  const { data } = await apiClient.post<PipelineTriggerResponse>(
    '/pipeline/trigger',
    null,
    { timeout: PIPELINE_TIMEOUT_MS },
  )
  return data
}

export async function uploadAndTriggerPipeline(files: File[]): Promise<PipelineUploadAndTriggerResponse> {
  const formData = buildUploadFormData(files)
  const { data } = await apiClient.post<PipelineUploadAndTriggerResponse>(
    '/pipeline/upload-and-trigger',
    formData,
    { timeout: PIPELINE_TIMEOUT_MS },
  )
  return data
}

export async function getPipelineStatus(runId: number): Promise<PipelineStatusResponse> {
  const { data } = await apiClient.get<PipelineStatusResponse>(`/pipeline/status/${runId}`, {
    timeout: 20000,
  })
  return data
}
```

`buildUploadFormData` is the **bug fix** from this chapter's research. The backend has two *named* fields, so each file is added under the right name based on its file name. See "Things to know" below.

### 5. `pages/DashboardPage.tsx`: the boss component

```tsx
import { useEffect, useState } from 'react'
import { getProducts, getStores } from '../api/forecast'
import type { Product, Store } from '../api/types'
import ProductStoreSelector from '../components/ProductStoreSelector'
import ForecastChart from '../components/ForecastChart'
import ExplanationPanel from '../components/ExplanationPanel'
import KPIBar from '../components/KPIBar'
import PipelineControl from '../components/PipelineControl'
import TrendBackdrop from '../components/TrendBackdrop'

function DashboardPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [stores, setStores] = useState<Store[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)

  const [selectedProductId, setSelectedProductId] = useState('')
  const [selectedStoreId, setSelectedStoreId] = useState('')

  useEffect(() => {
    Promise.all([getProducts(), getStores()])
      .then(([productList, storeList]) => {
        setProducts(productList)
        setStores(storeList)
      })
      .catch(() => setLoadError('Could not connect to backend.'))
  }, [])

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-top-row">
          <h1>Sales AI Forecast Tool</h1>
        </div>
        <p className="subtitle">Databricks-powered forecasts and explanations</p>
        <TrendBackdrop />
      </header>

      {loadError && <div className="banner error-banner">{loadError}</div>}

      <KPIBar />

      <PipelineControl />

      <ProductStoreSelector
        products={products}
        stores={stores}
        selectedProductId={selectedProductId}
        selectedStoreId={selectedStoreId}
        onSelectProduct={setSelectedProductId}
        onSelectStore={setSelectedStoreId}
      />

      <div className="dashboard-grid">
        <ForecastChart productId={selectedProductId} storeId={selectedStoreId} />

        {selectedProductId && selectedStoreId ? (
          <ExplanationPanel
            key={`${selectedProductId}-${selectedStoreId}`}
            productId={selectedProductId}
            storeId={selectedStoreId}
          />
        ) : (
          <div className="panel explanation-panel empty-state">
            <p>Select a product and store to explain the forecast.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default DashboardPage
```

Read the top of the function first: **four pieces of state**.

| State | Holds |
|---|---|
| `products`, `stores` | The lists for the drop-downs |
| `loadError` | A message if the backend is down |
| `selectedProductId`, `selectedStoreId` | What the user picked |

`useEffect(() => { ... }, [])`: the empty `[]` means "run **once**, after the first draw". It fetches both lists together with `Promise.all`.

**State lifting.** The two selected ids live **here**, in the parent, because *two* children need them: the chart and the explanation panel. The selector gets the ids and two "callbacks" (`onSelectProduct`, `onSelectStore`) to change them. This pattern, *data flows down, events flow up*, is the heart of React.

`key={`${selectedProductId}-${selectedStoreId}`}` on `ExplanationPanel` is a neat trick: when the key changes, React **throws away the old panel and creates a fresh one**, so an old explanation never stays on screen for a different product.

### 6. `ProductStoreSelector.tsx`: a "controlled" form

```tsx
import type { Product, Store } from '../api/types'

interface ProductStoreSelectorProps {
  products: Product[]
  stores: Store[]
  selectedProductId: string
  selectedStoreId: string
  onSelectProduct: (productId: string) => void
  onSelectStore: (storeId: string) => void
}

function ProductStoreSelector({
  products,
  stores,
  selectedProductId,
  selectedStoreId,
  onSelectProduct,
  onSelectStore,
}: ProductStoreSelectorProps) {
  return (
    <div className="panel selector">
      <label className="selector-field">
        <span>Product</span>
        <select value={selectedProductId} onChange={(event) => onSelectProduct(event.target.value)}>
          <option value="">Select a product…</option>
          {products.map((product) => (
            <option key={product.product_id} value={product.product_id}>
              {product.product_name} ({product.category})
            </option>
          ))}
        </select>
      </label>

      <label className="selector-field">
        <span>Store</span>
        <select value={selectedStoreId} onChange={(event) => onSelectStore(event.target.value)}>
          <option value="">Select a store…</option>
          {stores.map((store) => (
            <option key={store.store_id} value={store.store_id}>
              {store.store_name} ({store.city})
            </option>
          ))}
        </select>
      </label>
    </div>
  )
}

export default ProductStoreSelector
```

`interface ...Props` is the TypeScript contract: *this component needs these six things*. The `<select>` is **controlled**: its `value` comes from props and `onChange` reports back to the parent. `.map()` turns each product into an `<option>`. `key` helps React track list items.

### 7. `KPIBar.tsx` and `useCountUp.ts`

```ts
import { useEffect, useRef, useState } from 'react'

/** Animates from the previous value (or 0) up to `target` whenever it changes.
 * Returns null until the first real value arrives, so callers can keep
 * showing a loading placeholder instead of an animated "0". */
export function useCountUp(target: number | null, durationMs = 900): number | null {
  const [value, setValue] = useState<number | null>(null)
  const lastTarget = useRef(0)

  useEffect(() => {
    if (target === null) return

    const from = lastTarget.current
    const start = performance.now()
    let raf: number

    function tick(now: number) {
      const progress = Math.min((now - start) / durationMs, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(from + (target! - from) * eased)
      if (progress < 1) {
        raf = requestAnimationFrame(tick)
      } else {
        lastTarget.current = target!
      }
    }

    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [target, durationMs])

  return value
}
```

A **custom hook**: it animates a number from the old value to the new one over about a second, with an "ease-out" curve (`1 - (1 - progress)^3`). It uses `requestAnimationFrame` (the browser's "next frame" callback) and **cleans up** in the returned function so no animation keeps running after the component disappears. It returns `null` until the first real value arrives, so the screen shows `…` rather than an animated `0`.

`KPIBar.tsx` (about 130 lines) is long mostly because of four small SVG icons. The logic is the first 70 lines:

```tsx
function KPIBar() {
  const [kpis, setKpis] = useState<KPISummary | null>(null)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    setError(false)
    getKPIs()
      .then(setKpis)
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const categoryUnits = useCountUp(kpis?.top_category.total_units ?? null)
  const productUnits = useCountUp(kpis?.top_product.total_units ?? null)
  const atRiskCount = useCountUp(kpis ? kpis.at_risk_count : null, 700)
  const revenue = useCountUp(kpis?.predicted_revenue.total_predicted_revenue ?? null, 1200)

  if (error) {
    return (
      <div className="banner error-banner kpi-error">
        <span>Could not load KPI summary.</span>
        <button type="button" className="chip" onClick={load} disabled={loading}>
          {loading ? 'Retrying…' : 'Retry'}
        </button>
      </div>
    )
  }
```

- Three pieces of state: `kpis`, `error`, `loading`.
- `load` is wrapped in `useCallback`, so the same function is reused and can be called both by the effect **and** the Retry button.
- `useCountUp(...)` is called once per number. (Hooks must always be called, never inside an `if`.)
- On error we return a small banner with **Retry** instead of the tiles.

### 8. `ForecastChart.tsx`: fetch when the selection changes

```tsx
function ForecastChart({ productId, storeId }: ForecastChartProps) {
  const [points, setPoints] = useState<TrendPoint[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!productId || !storeId) {
      setPoints([])
      setError(null)
      return
    }

    let cancelled = false
    setLoading(true)
    setError(null)

    getForecastWithHistory(productId, storeId, 90)
      .then((response) => {
        if (!cancelled) setPoints(response.points)
      })
      .catch(() => {
        if (!cancelled) setError('Could not load forecast data.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [productId, storeId])

  if (!productId || !storeId) {
    return (
      <div className="panel chart-panel empty-state">
        <p>Select a product and store to see the forecast.</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="panel chart-panel empty-state">
        <span className="spinner" aria-label="Loading forecast" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="panel chart-panel empty-state">
        <p className="error-text">{error}</p>
      </div>
    )
  }

  // The history/forecast boundary is the last date with a real actual value,
  // not the real wall-clock "today" -- this dataset's calendar is simulated
  // and won't generally line up with whenever the dashboard happens to be viewed.
  const boundaryDate = [...points].reverse().find((point) => point.actual_units !== null)?.date

  return (
```

Study this effect:

```tsx
useEffect(() => { ... }, [productId, storeId])
```

The list at the end is the **dependency list**: React re-runs the effect whenever the product or store changes. Inside, `let cancelled = false` and the cleanup `return () => { cancelled = true }` solve a classic bug: if you click quickly from product A to product B, the slow answer for A could arrive *after* B and overwrite it. With `cancelled`, an outdated answer is ignored.

Then the component shows one of four things: a hint (nothing selected), a spinner, an error, or the chart. The line `boundaryDate = ...find(actual_units !== null)` finds the **last day with a real value**; that is where the "Today" marker is drawn. (It is *not* the computer's clock, because the dataset is simulated and ends on 2025-12-31.)

The chart itself (recharts) is declarative: two `<Area>` elements, one for `actual_units` (green) and one for `predicted_units` (orange, dashed), with `connectNulls={false}` so the lines **do not join** across the gap.

### 9. `ExplanationPanel.tsx`

```tsx
function describeError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNABORTED') {
      return 'The request timed out waiting for a response. Please try again.'
    }
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (error.response) return `Request failed (${error.response.status}).`
  }
  return 'Could not generate an explanation. Please try again.'
}

function ExplanationPanel({ productId, storeId }: ExplanationPanelProps) {
  const [generalResult, setGeneralResult] = useState<ForecastExplanation | null>(null)
  const [generalLoading, setGeneralLoading] = useState(false)
  const [generalError, setGeneralError] = useState<string | null>(null)

  async function handleExplain() {
    setGeneralLoading(true)
    setGeneralError(null)
    try {
      const result = await explainForecast(productId, storeId)
      setGeneralResult(result)
    } catch (error) {
      setGeneralError(describeError(error))
    } finally {
      setGeneralLoading(false)
    }
  }

  return (
    <div className="panel explanation-panel">
      <h2>Explain this forecast</h2>

      <button type="button" className="counter" onClick={handleExplain} disabled={generalLoading}>
        {generalLoading ? 'Generating…' : 'Explain this forecast'}
      </button>

      {generalError && <p className="error-text">{generalError}</p>}
      {generalResult && <ExplanationBody result={generalResult} />}
    </div>
  )
}

export default ExplanationPanel
```

- `describeError` turns an axios error into a friendly sentence: timeout, the backend's own `detail` text, or a generic message. This is the React twin of `ApiError` in the Streamlit app.
- `handleExplain` uses `try / catch / finally`: set *loading*, call the backend, save the result or the error, and **always** clear *loading*.
- `ReactMarkdown` renders the AI's text. The AI may use simple Markdown such as `**bold**` or bullet points.
- `result.forecast_summary` fills three number cards. As in [Chapter 13](13-genai.md), these come from the backend's computed facts, not from the AI's wording.

### 10. `PipelineControl.tsx`: upload and live status

![Retrain panel](../images/screenshots/ch14-react-pipeline.png)

The core is **polling**: ask "are you done yet?" on a timer.

![Polling](../images/diagrams/ch14-03-polling.svg)

```tsx
function PipelineControl() {
  const [filePicks, setFilePicks] = useState<FilePick[]>([])
  const [runId, setRunId] = useState<number | null>(null)
  const [status, setStatus] = useState<PipelineStatusResponse | null>(null)
  const [busy, setBusy] = useState(false)
  const [actionError, setActionError] = useState<string | null>(null)

  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  function stopPolling() {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  function startPolling(newRunId: number) {
    stopPolling()
    setRunId(newRunId)
    setStatus(null)
    setBusy(true)

    const poll = async () => {
      try {
        const result = await getPipelineStatus(newRunId)
        setStatus(result)
        if (TERMINAL_STATES.includes(result.life_cycle_state)) {
          stopPolling()
          setBusy(false)
        }
      } catch (error) {
        stopPolling()
        setBusy(false)
        setActionError(describeError(error))
      }
    }

    void poll()
    pollRef.current = setInterval(poll, POLL_INTERVAL_MS)
  }

  useEffect(() => stopPolling, [])
```

| Piece | Why |
|---|---|
| `useRef(...)` for the timer | A *ref* remembers a value **without** redrawing the screen when it changes. Perfect for an interval id |
| `startPolling` | Saves the run id, sets `busy`, polls **once immediately**, then every 4 seconds |
| `TERMINAL_STATES` | `TERMINATED`, `SKIPPED`, `INTERNAL_ERROR` mean "no more changes" → stop |
| `useEffect(() => stopPolling, [])` | Clean-up: if you leave the page, the timer stops |

`validateFilename` and `statusLabel` (top of the file) are the same rules as the Streamlit version: `.csv` and an allowed prefix, and a friendly word for each Databricks state.

### 11. `ChatPanel.tsx`: a small chat engine

```tsx
  async function runTurn(question: string, task: () => Promise<{ answer: string }>) {
    if (busy) return
    setBusy(true)

    const userId = `${Date.now()}-u`
    const assistantId = `${Date.now()}-a`
    setTurns((prev) => [
      ...prev,
      { id: userId, role: 'user', content: question },
      { id: assistantId, role: 'assistant', content: '', pending: true },
    ])

    try {
      const result = await task()
      setTurns((prev) =>
        prev.map((turn) => (turn.id === assistantId ? { ...turn, content: result.answer, pending: false } : turn)),
      )
    } catch (error) {
      setTurns((prev) =>
        prev.map((turn) =>
          turn.id === assistantId ? { ...turn, pending: false, error: describeError(error) } : turn,
        ),
      )
    } finally {
      setBusy(false)
    }
  }
```

`runTurn` is used by **every** button and by the text box:

1. Ignore the click if already `busy`.
2. Add *two* turns at once: the user's question and an empty assistant turn with `pending: true` (shown as a spinner).
3. Await the backend call (`task`), then find the pending turn by id and fill in the answer, or the error.
4. Always set `busy` back to false.

`setTurns((prev) => ...)` is the safe way to update state from the previous value. `bottomRef.scrollIntoView` keeps the newest message visible.

`handleSend` builds the **history** that goes to `/chat`, skipping turns that are pending or ended in errors.

![Analytics chat](../images/screenshots/ch14-react-chat.png)

### 12. `AnalyticsChatPage.tsx`

The page loads the lists, computes the unique category names with `useMemo` (so it is not recomputed on every draw) and passes them, with the optional store, to `ChatPanel`.

```tsx
  const categories = useMemo(() => [...new Set(products.map((product) => product.category))], [products])
  const selectedStoreName = stores.find((store) => store.store_id === selectedStoreId)?.store_name ?? ''
```

### 13. `TrendBackdrop.tsx` and the CSS

`TrendBackdrop.tsx` is a **purely decorative** animated line in the page header (`aria-hidden`, and it respects the user's *reduced motion* setting). The look comes from `index.css` (colours and variables like `--accent`) and `App.css` (layout). Skim them last; they change how the app looks, not what it does.

---

## ⚙️ `VITE_API_BASE_URL`: the surprise

![Build-time variable](../images/diagrams/ch14-04-env-build-time.svg)

A browser cannot read your `.env` file. Vite **copies the value into the JavaScript** when it starts (dev) or builds (production). Two consequences:

1. In dev, after editing `.env`, **stop and restart** `npm run dev`.
2. In production, changing an environment variable on the running server does **nothing**. You must **rebuild** with the new address.

> 🔐 **Never put secrets in a `VITE_` variable.** Anything inside is visible to every visitor. API keys stay in the backend.

---

## 🐳 Build and run in Docker

```docker
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Vite inlines VITE_* variables into the static bundle at BUILD time, so this
# must be a build arg (not just a runtime env var) to take effect.
ARG VITE_API_BASE_URL=http://localhost:8080
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

This is a **two-stage build**. Stage 1 (`node:22-alpine`) installs packages and runs `npm run build`. Stage 2 (`nginx:alpine`) keeps **only** the finished files in `dist/`, so the final image is small and has no Node.js in it.

```bash
docker build -t sales-ai-react --build-arg VITE_API_BASE_URL=http://localhost:8000 .
docker run -p 8080:80 sales-ai-react
```

Open <http://localhost:8080>. The backend must allow that address in `ALLOWED_ORIGINS`: add `http://localhost:8080`.

> ⚠️ The Dockerfile's **default** is `http://localhost:8080`, but the backend listens on **8000**. Always pass `--build-arg` as above (or change the default). More in [Chapter 16](16-docker-and-container-apps.md).

---

## 🛠️ Common problems

| Symptom | Cause | Fix |
|---|---|---|
| Red banner *Could not connect to backend* | Backend not running or wrong URL | Start it; check `VITE_API_BASE_URL`; restart `npm run dev` |
| Console: *blocked by CORS policy* | The page's address is not in `ALLOWED_ORIGINS` | Add it (comma separated), restart the backend |
| `npm install` fails | Old Node.js | Use Node 22 |
| Blank page after Docker build | Wrong backend URL was baked in | Rebuild with `--build-arg` |
| Upload says *No files provided.* | Old client with field name `files` | Use the current `pipeline.ts` |
| Changing `.env` has no effect | Value is read at start/build | Restart dev server or rebuild |
| TypeScript error after changing an API | `types.ts` no longer matches the JSON | Update `types.ts` |
| Chart is empty | No forecast rows for that product/store | Run the pipeline (real) or pick another pair |

---

## 🔎 Things to know (honest notes)

- **Bug found and fixed while writing this book:** the original `uploadAndTriggerPipeline` sent files under the field name `files`. The backend has two named fields, so the real endpoint replied *"No files provided."* The fix (`buildUploadFormData`) is in this repository. Lesson: test uploads against the **real** API, not only the mock.
- **A dead function remains.** `uploadPipelineFiles` in `pipeline.ts` posts to `/pipeline/upload`, which does not exist in the backend. Nothing calls it. Delete it in your own copy.
- **One file per kind.** The backend takes at most one sales file and one calendar file per upload. The React screen does not stop you from choosing two of the same kind; the backend would use only one of them (the Streamlit screen does check this).
- **No custom question for Explain.** The backend supports `user_question`, and `explainForecast()` accepts it, but the panel has no text box. Streamlit adds one.
- **No "data tools used" line.** The chat API returns `functions_used`, which this screen does not show.
- **No login.** Anyone who can open the page can retrain the model (Chapter 18).
- **Labels.** The chart marker says "Today", but it is the last day of data, not the calendar day.

---

## ✅ Checkpoint

1. What is the difference between **props** and **state**?
2. Why does `DashboardPage` own `selectedProductId`, instead of `ForecastChart`?
3. What does the empty `[]` at the end of `useEffect(..., [])` mean? What if it contains `[productId, storeId]`?
4. Why is `VITE_API_BASE_URL` "fixed at build time"?
5. Why does polling stop when the state is `TERMINATED`?

---

## 🔗 Learn more

- [React: Quick start](https://react.dev/learn)
- [React: useState and useEffect](https://react.dev/learn/synchronizing-with-effects)
- [React: Sharing state between components](https://react.dev/learn/sharing-state-between-components)
- [TypeScript for beginners](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- [Vite: env variables and modes](https://vite.dev/guide/env-and-mode)
- [React Router](https://reactrouter.com/)
- [axios](https://axios-http.com/docs/intro)
- [Recharts](https://recharts.org/)
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

⬅️ [Chapter 13](13-genai.md) · ➡️ **Next:** [Chapter 15: Frontend B, Streamlit](15-frontend-streamlit.md)
