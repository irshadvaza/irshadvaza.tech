# Domain 2: Implement Machine Learning Model Lifecycle and Operations (25–30%)

⬅ [Previous: Domain 1](./01-Domain1-MLOps-Infrastructure.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 3 – GenAIOps Infrastructure](./03-Domain3-GenAIOps-Infrastructure.md)

---

## 🧭 Domain Overview

**This is the single biggest domain on the exam (25–30%).** It covers the entire journey of a traditional ML model: **train → track → register → deploy → monitor → retrain.** If you only have time to deeply master one domain, make it this one.

Four sub-topics:
1. Orchestrate model training
2. Implement model registration and versioning
3. Deploy machine learning models for production environments
4. Monitor and maintain machine learning models in production

---

## 1️⃣ Orchestrate Model Training

### 🔑 Plain-English Explanation

"Orchestrating training" means moving beyond a single notebook cell run by hand, toward **repeatable, trackable, and scalable** training — whether that's one script, a hyperparameter sweep, or a full pipeline with multiple steps.

| Concept | What it does |
|---|---|
| **MLflow tracking** | Auto-logs metrics, parameters, artifacts, and models during training runs |
| **Automated ML (AutoML)** | Automatically tries multiple algorithms/hyperparameters to find the best model |
| **Notebooks** | Used for exploration, not production training (should graduate to scripts/pipelines) |
| **Hyperparameter tuning (sweep jobs)** | Automates search over hyperparameter space (grid, random, Bayesian) |
| **Distributed training** | Splits training across multiple nodes/GPUs for large/deep learning models |
| **Training pipelines** | Multi-step, reusable, versioned workflows (data prep → train → evaluate) |
| **Job comparison** | Compare metrics across runs in the Studio or via MLflow to pick the best model |

### 🏗️ Real-World Artifact — MLflow-Tracked Training Job

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

mlflow.autolog()  # auto-logs params, metrics, and the model artifact

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=200, max_depth=8)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    mlflow.log_metric("test_accuracy", acc)
```

```yaml
# sweep-job.yml — hyperparameter tuning
type: sweep
trial: ./train.yml
sampling_algorithm: bayesian
search_space:
  max_depth:
    type: choice
    values: [4, 6, 8, 10]
  n_estimators:
    type: choice
    values: [100, 200, 300]
objective:
  goal: maximize
  primary_metric: test_accuracy
limits:
  max_total_trials: 20
  max_concurrent_trials: 4
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| `mlflow.autolog()` | Captures params/metrics/model with minimal code |
| Sampling algorithms for sweeps | Grid, Random, **Bayesian** (learns from past trials — most sample-efficient) |
| Distributed training frameworks | PyTorch DDP, Horovod, DeepSpeed — orchestrated via Azure ML distributed job config |
| Pipeline vs. single job | Pipeline = multiple **components** chained together with defined inputs/outputs |

---

### ❓ Practice Questions — Orchestrate Model Training

**Q1.** You are running a hyperparameter sweep with a large search space and want to minimize the number of trials needed to find near-optimal hyperparameters by learning from the results of previous trials. Which sampling algorithm should you choose?

A) Grid sampling
B) Random sampling
C) Bayesian sampling
D) Exhaustive sampling

✅ **Answer: C) Bayesian sampling**

💡 **Explanation:** **Bayesian sampling** picks each new set of hyperparameters based on how previous trials performed, converging toward good results in **fewer trials** than grid (which tries every combination) or random (which ignores past results entirely). This directly matches "minimize number of trials … by learning from previous trials."

---

**Q2.** A data scientist wants every training run — parameters, metrics, and the resulting model file — automatically captured without manually writing logging code for each value. What should they add to their training script?

A) `print()` statements for each metric
B) `mlflow.autolog()`
C) A custom logging framework written from scratch
D) Save metrics to a local CSV file

✅ **Answer: B) `mlflow.autolog()`**

💡 **Explanation:** MLflow's **autologging** automatically captures parameters, metrics, and the model artifact for supported ML frameworks (scikit-learn, PyTorch, etc.) with a single line of code — this is the exam's expected "path of least resistance" for experiment tracking, versus manual instrumentation.

---

**Q3.** Your organization trains a large deep learning model that takes 30 hours on a single GPU. You need to reduce training time significantly by splitting the workload across multiple GPU nodes. What should you configure?

A) A Compute Instance with more disk space
B) A distributed training job across a multi-node GPU compute cluster
C) A batch inference endpoint
D) AutoML with a shorter experiment timeout

✅ **Answer: B) A distributed training job across a multi-node GPU compute cluster**

💡 **Explanation:** Reducing wall-clock training time for large/deep learning models requires **distributed training** (data-parallel or model-parallel) across multiple nodes/GPUs, which Azure ML supports via distributed job configurations (e.g., PyTorch DDP). Compute Instances are single-node dev environments and can't be split across nodes.

---

## 2️⃣ Implement Model Registration and Versioning

### 🔑 Plain-English Explanation

Once you have a model you like, you **register** it — giving it a name, version number, and metadata so it can be deployed, audited, and rolled back reliably. This sub-topic also covers **Responsible AI evaluation** and **lifecycle management** (including retiring old models).

| Concept | What it means |
|---|---|
| **Feature retrieval spec + model artifact** | Bundling the exact feature-engineering logic with the model so training/serving stay consistent (no train/serve skew) |
| **Register an MLflow model** | MLflow's standard model format registers cleanly with full lineage back to the training run |
| **Responsible AI evaluation** | Fairness, interpretability/explainability, error analysis before promoting a model |
| **Model lifecycle / archiving** | Versions move through stages; old/underperforming versions get archived, not silently deleted |

### 🏗️ Real-World Artifact — Registering a Model

```bash
az ml model create \
  --name fraud-detector \
  --version 4 \
  --path ./outputs/model \
  --type mlflow_model \
  --resource-group rg-ai300-demo \
  --workspace-name mlw-fraud-detection
```

```python
# Responsible AI: quick fairness check
from raiwidgets import FairnessDashboard
FairnessDashboard(sensitive_features=test_df["region"],
                   y_true=y_test, y_pred=model.predict(X_test))
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| MLflow model registration | Preserves full lineage: run → model → deployment |
| Responsible AI dashboard covers | Error analysis, fairness, explainability (SHAP-based), causal analysis |
| Archiving | Keeps history/audit trail vs. hard-deleting a version |
| Feature retrieval spec | Prevents **training/serving skew** by reusing the same feature logic at inference time |

---

### ❓ Practice Questions — Model Registration & Versioning

**Q4.** Your credit-scoring model performs well overall, but you're concerned it might treat applicants from different regions unfairly. Before registering the model for production deployment, what should you do?

A) Deploy immediately since overall accuracy is high
B) Run a Responsible AI fairness evaluation across the sensitive feature (region) before registering
C) Remove the region column from the dataset after deployment
D) Only check the confusion matrix on the full test set

✅ **Answer: B) Run a Responsible AI fairness evaluation across the sensitive feature (region) before registering**

💡 **Explanation:** The exam explicitly calls out **"Evaluate a model by using responsible AI principles"** as a registration-stage step. A high aggregate accuracy can mask disparate performance across subgroups; a fairness evaluation (e.g., via the Responsible AI dashboard) surfaces this **before** the model is promoted, not after deployment when harm has already occurred.

---

**Q5.** You retrained a fraud-detection model and it now underperforms the currently deployed version. You still need to retain the old version for audit and potential rollback, but don't want it cluttering the "active" model list. What should you do?

A) Permanently delete the old version
B) Archive the old model version
C) Rename the old version to "deprecated_v1"
D) Move the model file to a personal OneDrive folder

✅ **Answer: B) Archive the old model version**

💡 **Explanation:** **Archiving** is the designed lifecycle action for models no longer active but still needed for audit/rollback/compliance — it keeps full version history and lineage intact, unlike deletion (which is irreversible and destroys audit trail) or informal renaming (not a governed lifecycle state).

---

**Q6.** Why should you package a feature retrieval specification together with the model artifact when registering a model?

A) It reduces the model file size
B) It ensures the same feature-engineering logic used in training is applied consistently at inference time, preventing training/serving skew
C) It automatically improves model accuracy
D) It is required for MLflow autologging to function

✅ **Answer: B) It ensures the same feature-engineering logic used in training is applied consistently at inference time, preventing training/serving skew**

💡 **Explanation:** **Training/serving skew** — where features are computed differently at training time vs. real-time inference — is a classic production ML failure mode. Bundling the feature retrieval spec with the model artifact guarantees the exact same transformation logic runs in both places.

---

## 3️⃣ Deploy Machine Learning Models for Production Environments

### 🔑 Plain-English Explanation

Two primary deployment shapes, plus the mechanics of doing it safely:

| Endpoint Type | Use Case | Latency |
|---|---|---|
| **Real-time (online) endpoint** | Synchronous, low-latency predictions (e.g., fraud check on checkout) | Milliseconds–seconds |
| **Batch endpoint** | Large-volume, asynchronous scoring (e.g., nightly scoring of all customers) | Minutes–hours |

**Progressive rollout / safe rollback** = don't flip 100% of traffic to a new model version at once.

### 🏗️ Real-World Artifact — Blue/Green Traffic Split for Safe Rollout

```yaml
# managed online endpoint traffic allocation
name: fraud-detector-endpoint
traffic:
  blue: 90    # current stable version — 90% of traffic
  green: 10   # new candidate version — 10% canary traffic
```

```bash
# After validating green's metrics look good, shift traffic gradually:
az ml online-endpoint update --name fraud-detector-endpoint \
  --traffic "blue=50 green=50"

# Full cutover once confident:
az ml online-endpoint update --name fraud-detector-endpoint \
  --traffic "blue=0 green=100"

# Instant rollback if something looks wrong:
az ml online-endpoint update --name fraud-detector-endpoint \
  --traffic "blue=100 green=0"
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Managed online endpoint | Fully managed compute + autoscaling for real-time inference |
| Batch endpoint compute | Uses compute clusters, scales out across nodes for large jobs |
| Testing endpoints | Use the built-in test tab / `az ml online-endpoint invoke` before production traffic |
| Rollout strategy | Canary/blue-green traffic-splitting on a single endpoint with multiple deployments |

---

### ❓ Practice Questions — Deployment

**Q7.** You need to score 5 million customer records overnight for a marketing model, and the results don't need to be available in real time. Which endpoint type is most appropriate and cost-effective?

A) Managed real-time (online) endpoint
B) Batch endpoint
C) A single Compute Instance running a Jupyter notebook manually
D) An always-on Kubernetes deployment with autoscale set to always-on

✅ **Answer: B) Batch endpoint**

💡 **Explanation:** **Batch endpoints** are purpose-built for large-volume, asynchronous scoring jobs — they scale out across a compute cluster, process data in parallel, and don't require an always-on, low-latency serving layer, making them far more cost-effective than a real-time endpoint for this scenario.

---

**Q8.** You've deployed a new version of a model behind the same online endpoint as the current production version. You want to send only 10% of live traffic to the new version to validate it before a full cutover, with the ability to instantly revert if something goes wrong. What deployment strategy does this describe?

A) Shadow deployment with no live traffic
B) Progressive rollout using traffic splitting (canary deployment)
C) A/B testing via two separate, unlinked endpoints
D) Immediate full cutover

✅ **Answer: B) Progressive rollout using traffic splitting (canary deployment)**

💡 **Explanation:** Allocating a small traffic percentage (e.g., 10%) to a new deployment on the **same endpoint**, monitoring it, then gradually increasing it — with the ability to set the percentage back to 0 instantly — is the textbook **canary/progressive rollout pattern**, explicitly named in the skills outline as "progressive rollout and safe rollback strategies."

---

## 4️⃣ Monitor and Maintain Machine Learning Models in Production

### 🔑 Plain-English Explanation

A model that was accurate on launch day can silently degrade as the real world changes — this is **data drift** (input distribution changes) or **concept drift** (the relationship between inputs and outputs changes). Monitoring closes the loop back to retraining.

| Concept | What it means |
|---|---|
| **Data drift detection** | Compares production input feature distributions vs. training baseline |
| **Performance monitoring** | Tracks accuracy/precision/recall (when ground truth becomes available), latency, error rate |
| **Retraining triggers** | Automated pipeline kicks off retraining when drift/performance crosses a threshold |
| **Alerting** | Notifies the team (email, Teams, PagerDuty via Azure Monitor) when thresholds are breached |

### 🏗️ Real-World Artifact — Drift Monitor + Alert (Conceptual YAML)

```yaml
# monitoring definition
monitoring_target:
  endpoint_deployment_id: azureml:fraud-detector-endpoint:blue
signals:
  data_drift:
    reference_data: azureml:training-data-baseline:1
    metric_thresholds:
      normalized_wasserstein_distance: 0.15
alert_notification:
  emails: ["mlops-team@contoso.com"]
schedule:
  frequency: day
  interval: 1
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Data drift vs. concept drift | Drift = input distribution shifts; concept drift = X→Y relationship shifts |
| Common drift metrics | Population Stability Index (PSI), Wasserstein distance, Jensen-Shannon divergence |
| Retraining trigger pattern | Monitor → threshold breach → auto-trigger retraining pipeline (via GitHub Actions/Azure ML pipeline schedule) |
| Where alerts land | Azure Monitor → action groups → email/Teams/webhook |

---

### ❓ Practice Questions — Monitoring & Maintenance

**Q9.** Three months after deployment, your model's predictions have become less accurate even though no code has changed. Investigation shows the distribution of customer ages in production has shifted significantly compared to the training data. What is this phenomenon called, and what should you configure to catch it earlier next time?

A) Concept drift; configure a batch endpoint
B) Data drift; configure a data drift monitoring signal comparing production data to the training baseline
C) Model overfitting; retrain with more epochs
D) Endpoint latency degradation; scale up compute

✅ **Answer: B) Data drift; configure a data drift monitoring signal comparing production data to the training baseline**

💡 **Explanation:** A shift in the **input feature distribution** (customer ages) relative to the training baseline is the definition of **data drift**. Azure ML's monitoring capability lets you define a data drift signal that compares live inference data against a reference (training) dataset on a schedule, catching this before it silently erodes accuracy.

---

**Q10.** You want your retraining pipeline to run automatically only when a monitored performance metric drops below an acceptable threshold, rather than on a fixed weekly schedule regardless of need. What should you configure?

A) A fixed cron schedule only
B) A monitoring signal with a metric threshold that triggers a retraining pipeline/alert when breached
C) Manual retraining triggered by emailing the data science team
D) Disable monitoring to save cost

✅ **Answer: B) A monitoring signal with a metric threshold that triggers a retraining pipeline/alert when breached**

💡 **Explanation:** The skills outline explicitly calls out **"Configure retraining or alert triggers when thresholds are exceeded."** Threshold-based, event-driven retraining is more efficient than blind fixed-schedule retraining — you retrain only when there's evidence it's needed, saving compute cost while staying responsive to real degradation.

---

## 🧠 Domain 2 Quick-Recall Cheat Sheet

- **Training**: `mlflow.autolog()`, Bayesian sweeps > grid/random for efficiency, distributed training for large models
- **Registration**: MLflow format, Responsible AI fairness check **before** registering, archive (don't delete) old versions
- **Deployment**: Real-time (online) endpoint = low latency; Batch endpoint = high volume/async; canary traffic-split for safe rollout
- **Monitoring**: Data drift = input distribution shift; set thresholds → auto-trigger retraining + alerts

---

⬅ [Previous: Domain 1](./01-Domain1-MLOps-Infrastructure.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 3 – GenAIOps Infrastructure](./03-Domain3-GenAIOps-Infrastructure.md)
