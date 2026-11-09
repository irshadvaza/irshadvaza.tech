# Chapter 1: The business problem

> 🎯 **What you will learn**
> - Why a shop needs a *forecast*, explained with a tiny example
> - What problems the Sales AI project solves, and for whom
> - How we will know the project worked (and what **WAPE** means)
> - What is *in* and *out* of this project

⏱️ Reading time: about 15 minutes. No code in this chapter.

---

## 🧸 Start with a tiny shop

Imagine you sell **ice cream** from a small shop. Every morning you decide how many tubs to order.

| If you order... | What happens | The cost |
|---|---|---|
| **Too many** | Tubs melt or sit unsold | Wasted money, markdowns |
| **Too few** | Customers arrive and you have none | Lost sales, unhappy customers |
| **Just right** | Almost everything sells | Happy customers, healthy profit |

You decide using memory: *"Last July was hot, so I will order more."* That works for one shop and one product.

Now imagine **8 shops** and **6 product categories**, with sales affected by holidays, weather, discounts and the economy. Memory and spreadsheets stop working. This is the real situation for most retailers, and it is the problem this project solves.

---

## 🏬 The real situation

Today, demand planning in many retail companies is **manual**. Planners build forecasts from last year's sales, personal experience and spreadsheets. Holidays, promotions and weather are accounted for inconsistently, if at all.

This causes three recurring problems:

1. **Overstock.** Slow-moving products tie up cash and end up on discount.
2. **Stockouts.** Popular or promoted items run out, so sales and customers are lost.
3. **Inconsistency.** Forecast quality depends on who made it, not on a shared, repeatable method.

![The three problems](../images/diagrams/01-three-problems.svg)

---

## 💡 The opportunity

The company already has the data: sales, products, stores, holidays, promotions. It is just not joined together into one trusted forecasting tool.

**Sales AI** joins it and adds two things:

- 🤖 **Machine learning** that predicts demand for the next **30 days**.
- 💬 **Generative AI (an LLM)** that explains the forecast in plain business language and answers questions.

> 🧠 **The most important design rule of the whole project**
> The ML model creates the numbers. The LLM only **explains** them.
> It is never allowed to invent or change a number. We build this rule into the code in [Chapter 13](13-genai.md).

---

## 👥 Who uses it?

| Person | What they want | Which screen |
|---|---|---|
| **Demand planner** | "What will we sell next month in this store?" | Forecast Dashboard |
| **Category manager** | "Which category is growing fastest? Which is at risk?" | Analytics Assistant (chat) |
| **Store operations manager** | "How is my store doing compared with others?" | Both |
| **Data and AI team** (you!) | Keep the data, model and AI layer running and accurate | Pipeline refresh |

---

## 🖥️ What the platform does

The platform has **two screens** and one background job.

### Screen 1: Forecast Dashboard
Pick a **category/product** and a **store**. You see:

- A chart with **past sales** and the **next 30 days of forecast** on one timeline, with a clear break between "what happened" and "what we predict".
- **KPI cards**: top-selling product, number of at-risk items, total predicted revenue and units.
- An **Explain** button that writes a short plain-English explanation: key drivers, risks or opportunities, and a recommended action.

![Dashboard screenshot](../images/screenshots/react-dashboard.png)

### Screen 2: Analytics Assistant (chat)
Ask free-text questions like *"Which category is growing fastest?"* or tap a **one-click question**. Answers come from **real data**. If the data to answer does not exist, the assistant says so instead of guessing.

### Background job: Data refresh and retraining
Upload a new month of sales data, press a button, and the pipeline **re-ingests, re-validates, retrains and re-forecasts**. A new model replaces the old one **only if it is better** on held-out data.

---

## 📏 How do we know it works?

We need a number for "how wrong is the forecast?". We use **WAPE** (Weighted Absolute Percentage Error).

### A worked example

Four days of real sales, and what a model predicted:

| Day | Actual sales | Forecast | Error (distance) |
|---|---|---|---|
| Mon | 10 | 12 | 2 |
| Tue | 0 | 3 | 3 |
| Wed | 20 | 15 | 5 |
| Thu | 10 | 10 | 0 |
| **Total** | **40** | | **10** |

```text
WAPE = total error / total actual sales
     = 10 / 40
     = 0.25  →  25%
```

**Lower is better.** 0% would be a perfect forecast.

> 🤔 **Why not the more common MAPE?**
> MAPE divides each day's error by that day's actual sales. On Tuesday the actual is **0**, and dividing by zero is impossible. Retail has many zero-sales days, so WAPE (which divides by the *total*) is the safer choice. You will see the code in [Chapter 9](09-model-training.md).

### The success tests

The project is a success if:

- ✅ The model has **clearly lower WAPE than a naive baseline** (in this project: "same weekday last week") on data it has never seen.
- ✅ A planner can read a forecast and its explanation **without asking an analyst**.
- ✅ A category manager can answer common questions through the chat.
- ✅ A new month of data can be uploaded and a fresh forecast produced **without a data engineer**.
- ✅ Any number on screen can be **traced back** to the data and model version that produced it.

---

## 🎚️ Scope: what is in and out

| ✅ In scope | ❌ Out of scope (this phase) |
|---|---|
| Load and clean sales, product, store and calendar data | Automatic ordering or purchase orders (we *recommend*, we do not *execute*) |
| 30-day forecast per product, store and day | Real-time forecasting (we refresh in batches) |
| Model registry: only validated models go live | Products and stores outside the pilot data |
| GenAI explanations and chat grounded in real data | Connecting directly to a live POS or ERP system |
| Dashboard and chat screens | A mobile app (the web app is responsive) |
| Upload new data and retrain from the app | |

---

## ⚠️ Risks the design already handles

| Risk | How the project handles it |
|---|---|
| The model gets worse over time as the market changes ("drift") | Retrain on new data; compare new vs current model before promoting |
| People trust the AI too much | The AI only explains real computed numbers; it is *decision support*, a human decides |
| Bad uploaded data ruins forecasts silently | Data is validated in the Silver layer; bad rows are flagged, not hidden |
| The tool feels like a "black box" | Every forecast comes with a plain-language explanation |

---

## 📖 Words to remember

| Word | Plain meaning |
|---|---|
| **Forecast horizon** | How many days ahead we predict. Here: **30**. |
| **WAPE** | Total forecast error divided by total actual sales. Lower is better. |
| **Stockout** | Customers wanted to buy, but the shelf was empty. Recorded sales then *understate* real demand. |
| **Model registry** | A versioned library of trained models, so we always know which one made a forecast. |
| **Grounded explanation** | An AI explanation that only uses numbers from real computed data. |
| **Pipeline refresh** | Re-load data, retrain the model, regenerate forecasts. |

---

## ✅ Checkpoint

You should now be able to answer, in your own words:

1. What three problems does manual forecasting cause?
2. What does the ML model do, and what does the LLM do?
3. If actual sales were 50 units in total and the total error was 10, what is the WAPE? *(Answer: 20%)*

---

## 🔗 Learn more

- [Demand forecasting basics (Wikipedia)](https://en.wikipedia.org/wiki/Demand_forecasting)
- [Forecast accuracy metrics, including WAPE (Wikipedia)](https://en.wikipedia.org/wiki/Mean_absolute_percentage_error)
- [Forecasting: Principles and Practice, a free online book](https://otexts.com/fpp3/)

➡️ **Next:** [Chapter 2: The big picture](02-big-picture.md)
