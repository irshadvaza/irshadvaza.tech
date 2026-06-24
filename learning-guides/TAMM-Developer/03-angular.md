# 🅰️ Module 3 — Angular for TAMM Developers

> **Prerequisites:** [Module 2 — React.js](./02-reactjs.md)  
> **Time to complete:** ~3 hours  
> **Next Module:** [04-service-lifecycle.md](./04-service-lifecycle.md)

---

## Table of Contents

1. [What is Angular?](#1-what-is-angular)
2. [React vs Angular — Which Does TAMM Use Where?](#2-react-vs-angular--which-does-tamm-use-where)
3. [Brief History of Angular](#3-brief-history-of-angular)
4. [Core Architecture](#4-core-architecture)
5. [Core Concepts](#5-core-concepts)
   - [5.1 Modules (NgModule)](#51-modules-ngmodule)
   - [5.2 Components](#52-components)
   - [5.3 Templates & Data Binding](#53-templates--data-binding)
   - [5.4 Services & Dependency Injection](#54-services--dependency-injection)
   - [5.5 Routing & Guards](#55-routing--guards)
   - [5.6 Reactive Forms](#56-reactive-forms)
   - [5.7 RxJS & Observables](#57-rxjs--observables)
   - [5.8 HttpClient](#58-httpclient)
6. [TAMM-Specific Patterns in Angular](#6-tamm-specific-patterns-in-angular)
   - [6.1 UAE Pass Auth Guard](#61-uae-pass-auth-guard)
   - [6.2 Bilingual Angular App (ngx-translate)](#62-bilingual-angular-app-ngx-translate)
   - [6.3 TAMM Service Form (Reactive Forms)](#63-tamm-service-form-reactive-forms)
   - [6.4 NgRx State for Journey Management](#64-ngrx-state-for-journey-management)
7. [Step-by-Step: Build a TAMM Portal Page](#7-step-by-step-build-a-tamm-portal-page)
8. [Best Practices](#8-best-practices)
9. [Summary & What's Next](#9-summary--whats-next)

---

## 1. What is Angular?

**Angular** is a complete, opinionated **framework** for building web applications. Developed and maintained by Google, it gives you everything in one package: component system, routing, HTTP client, forms, dependency injection, state management — all with TypeScript by default.

The key distinction from React:

| | React | Angular |
|---|---|---|
| Type | Library | Full Framework |
| Language | JavaScript (or TypeScript) | TypeScript only |
| What it includes | UI rendering only | Everything (routing, HTTP, forms, DI) |
| Opinion level | Low (you choose your tools) | High (the Angular way) |
| Learning curve | Gentler start | Steeper start, less decision fatigue |

> 💡 **The analogy:** React is a precision scalpel — lightweight, flexible, you choose what to pair it with. Angular is a fully-equipped surgical suite — everything is there, and everything works together.

---

## 2. React vs Angular — Which Does TAMM Use Where?

TAMM uses **both** — for different parts of the platform:

| Platform Part | Technology | Reason |
|---|---|---|
| TAMM main web portal (tamm.ae) | Angular | Large team, strong typing, enterprise patterns |
| TAMM mobile app | React Native | Shared logic with React web components |
| TAMM service micro-frontends | React | Rapid development, smaller isolated services |
| TAMM admin / backoffice | Angular | Complex forms, table-heavy data, strict typing |
| TAMM developer portal | React | Docs and sandbox tools |

Understanding both is essential for a TAMM developer. You will encounter Angular in the core portal and admin tools, and React in service-specific pages.

---

## 3. Brief History of Angular

### 2010 — AngularJS (Angular 1)

**Misko Hevery**, a Google engineer, created **AngularJS** in 2010 as a side project that made it dramatically easier to build single-page applications. Its "two-way data binding" was magical at the time — change a model, the view updates automatically. Change the view, the model updates.

AngularJS was adopted by thousands of government, enterprise, and startup applications worldwide. By 2012 it was one of the most starred projects on GitHub.

### 2014–2016 — The Rewrite Crisis

As AngularJS apps grew, performance problems emerged. The two-way binding's "dirty checking" mechanism — checking every value on every cycle — struggled with large datasets. Large TAMM-scale applications (with hundreds of form fields and real-time data) hit these limits.

Google announced a complete rewrite in 2014 — not AngularJS 2.0, but a brand-new framework: **Angular**. The community was split; it was controversial. The rewrite was justified: Angular (version 2+) is faster, more scalable, and better suited to enterprise applications.

### 2016 — Angular 2 Releases

Angular 2 released in September 2016. Key changes:

- **TypeScript** as the default language — bringing static typing, interfaces, and better tooling
- **Component-based architecture** replacing controllers and scope
- **Dependency Injection** as a first-class framework feature
- **RxJS** for reactive programming
- **Angular CLI** for project generation and building

### 2017 — Angular 4 and the Version Leap

Google skipped Angular 3 (to align package versions) and released Angular 4 — the first LTS-quality release. Enterprise adoption accelerated.

### 2018–2020 — Ivy Renderer

Angular 6–9 introduced **Ivy**, a complete rewrite of Angular's rendering engine. Ivy produces smaller bundles (critical for TAMM mobile users on limited data), compiles faster, and catches more errors at build time.

### 2022–Present — Angular 14–17: Standalone Components

Angular 14 introduced **standalone components** — eliminating the need for `NgModule` in many cases and making Angular simpler and closer to React's component model. Angular 17 (2023) brought a new `@if`, `@for` syntax in templates. TAMM's newer portal services use standalone components.

```
Angular Timeline

2010 ─── AngularJS (Misko Hevery, Google)
2016 ─── Angular 2 (complete rewrite; TypeScript; Component model)
2017 ─── Angular 4 (first stable enterprise version)
2019 ─── Angular 8 + Ivy preview
2020 ─── Angular 9 (Ivy default; TAMM portal baseline)
2022 ─── Angular 14 (Standalone components)
2023 ─── Angular 17 (new template syntax; TAMM upgrade path)
```

---

## 4. Core Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    ANGULAR APPLICATION                    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │                  APP MODULE                      │    │
│  │  ┌─────────────┐  ┌─────────────┐               │    │
│  │  │  Routing    │  │  Shared     │               │    │
│  │  │  Module     │  │  Module     │               │    │
│  │  └──────┬──────┘  └─────┬───────┘               │    │
│  │         │               │                        │    │
│  │  ┌──────▼───────────────▼──────────────────┐    │    │
│  │  │           COMPONENTS                     │    │    │
│  │  │  Template (HTML) + Class (TS) + CSS      │    │    │
│  │  └──────────────────┬───────────────────────┘    │    │
│  │                     │ injects                    │    │
│  │  ┌──────────────────▼───────────────────────┐    │    │
│  │  │           SERVICES (DI)                  │    │    │
│  │  │  ApplicationService │ AuthService        │    │    │
│  │  │  DocumentService    │ TranslationService │    │    │
│  │  └──────────────────┬───────────────────────┘    │    │
│  │                     │                            │    │
│  │  ┌──────────────────▼───────────────────────┐    │    │
│  │  │           HTTP CLIENT                    │    │    │
│  │  │       (calls TAMM Node.js APIs)          │    │    │
│  │  └──────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Core Concepts

### 5.1 Modules (NgModule)

An Angular **module** is a container that groups related components, directives, pipes, and services. Every Angular app has at least one module: `AppModule`.

```typescript
// src/app/app.module.ts

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ServiceListComponent } from './services/service-list/service-list.component';
import { ApplicationFormComponent } from './applications/application-form/application-form.component';

// Feature module for application-related components
import { ApplicationsModule } from './applications/applications.module';

@NgModule({
  declarations: [
    AppComponent,
    ServiceListComponent,
    // Standalone components are NOT declared here — they import themselves
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,       // Required for HttpClient
    ReactiveFormsModule,    // Required for reactive forms
    ApplicationsModule      // Feature module
  ],
  providers: [],           // Services provided at root level go in @Injectable({ providedIn: 'root' })
  bootstrap: [AppComponent]
})
export class AppModule {}
```

---

### 5.2 Components

An Angular component = TypeScript class + HTML template + CSS styles.

```typescript
// src/app/services/service-card/service-card.component.ts

import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

interface TammService {
  id: string;
  name: { en: string; ar: string };
  category: string;
  fee: number;
  processingDays: number;
  isPopular: boolean;
}

@Component({
  selector: 'app-service-card',          // Use as <app-service-card> in templates
  templateUrl: './service-card.component.html',
  styleUrls: ['./service-card.component.scss']
})
export class ServiceCardComponent implements OnInit {
  @Input() service!: TammService;        // Data coming IN from parent
  @Input() language: 'en' | 'ar' = 'en';
  @Output() applyClicked = new EventEmitter<string>();  // Events going OUT to parent

  serviceName = '';
  categoryColor = '';

  private readonly categoryColors: Record<string, string> = {
    'Construction': '#E67E22',
    'Business': '#2980B9',
    'Healthcare': '#27AE60',
    'Civil': '#8E44AD'
  };

  ngOnInit(): void {
    this.serviceName = this.language === 'ar'
      ? this.service.name.ar
      : this.service.name.en;
    this.categoryColor = this.categoryColors[this.service.category] || '#95A5A6';
  }

  onApplyClick(): void {
    this.applyClicked.emit(this.service.id);
  }
}
```

```html
<!-- service-card.component.html -->

<div class="service-card" [class.rtl]="language === 'ar'">
  <div class="card-badge" [style.color]="categoryColor">
    {{ service.category }}
    <span *ngIf="service.isPopular" class="popular-tag">⭐ Popular</span>
  </div>

  <h3 class="card-title">{{ serviceName }}</h3>

  <div class="card-meta">
    <span class="fee">
      💰 {{ service.fee === 0 ? (language === 'ar' ? 'مجاني' : 'Free') : (service.fee + ' AED') }}
    </span>
    <span class="days">
      ⏱ {{ service.processingDays }} {{ language === 'ar' ? 'أيام' : 'days' }}
    </span>
  </div>

  <button class="apply-btn" (click)="onApplyClick()">
    {{ language === 'ar' ? 'تقدم الآن ←' : 'Apply Now →' }}
  </button>
</div>
```

---

### 5.3 Templates & Data Binding

Angular templates support four types of data binding:

```html
<!-- 1. INTERPOLATION — display data in the template -->
<h1>{{ applicationId }}</h1>
<p>Status: {{ application.status | titlecase }}</p>

<!-- 2. PROPERTY BINDING — set an element's property from component data -->
<input [value]="searchQuery" />
<button [disabled]="isSubmitting">Submit</button>
<img [src]="service.iconUrl" [alt]="service.name.en" />

<!-- 3. EVENT BINDING — call component methods on user events -->
<button (click)="onSubmit()">Submit Application</button>
<input (input)="onSearch($event)" />
<form (ngSubmit)="handleFormSubmit()">

<!-- 4. TWO-WAY BINDING — sync form fields with component properties -->
<input [(ngModel)]="searchQuery" />
<!-- Same as: [value]="searchQuery" (input)="searchQuery = $event.target.value" -->
```

#### Structural Directives

```html
<!-- *ngIf — conditional rendering -->
<div *ngIf="application; else loading">
  <h2>{{ application.id }}</h2>
</div>
<ng-template #loading>
  <app-loading-spinner></app-loading-spinner>
</ng-template>

<!-- *ngFor — list rendering -->
<div *ngFor="let service of services; let i = index; trackBy: trackByServiceId">
  <app-service-card [service]="service" [language]="currentLanguage"></app-service-card>
</div>

<!-- *ngSwitch — multiple condition rendering -->
<div [ngSwitch]="application.status">
  <app-review-banner *ngSwitchCase="'under_review'"></app-review-banner>
  <app-approved-banner *ngSwitchCase="'approved'"></app-approved-banner>
  <app-rejected-banner *ngSwitchCase="'rejected'"></app-rejected-banner>
  <app-default-status *ngSwitchDefault></app-default-status>
</div>

<!-- Angular 17+ new syntax (no asterisk) -->
@if (application) {
  <h2>{{ application.id }}</h2>
} @else {
  <app-loading-spinner />
}

@for (service of services; track service.id) {
  <app-service-card [service]="service" />
}
```

---

### 5.4 Services & Dependency Injection

A **service** is a TypeScript class that holds business logic or data access. **Dependency Injection (DI)** means Angular creates services for you and injects them into components automatically.

```typescript
// src/app/core/services/application.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface Application {
  id: string;
  serviceId: string;
  serviceName: string;
  status: string;
  submittedAt: string;
}

@Injectable({
  providedIn: 'root'   // ← Singleton: one instance shared across the whole app
})
export class ApplicationService {
  private readonly apiBase = `${environment.tammApiUrl}/api/v1`;

  constructor(private http: HttpClient) {}

  getAllApplications(): Observable<Application[]> {
    return this.http
      .get<{ success: boolean; data: Application[] }>(`${this.apiBase}/applications`)
      .pipe(
        map(response => response.data),
        catchError(err => {
          console.error('Failed to fetch applications:', err);
          return throwError(() => new Error(err.message));
        })
      );
  }

  getApplicationById(id: string): Observable<Application> {
    return this.http
      .get<{ success: boolean; data: Application }>(`${this.apiBase}/applications/${id}`)
      .pipe(map(response => response.data));
  }

  submitApplication(payload: Partial<Application>): Observable<Application> {
    return this.http
      .post<{ success: boolean; data: Application }>(`${this.apiBase}/applications`, payload)
      .pipe(map(response => response.data));
  }
}
```

```typescript
// Injecting the service into a component

@Component({ selector: 'app-dashboard', templateUrl: './dashboard.component.html' })
export class DashboardComponent implements OnInit {
  applications: Application[] = [];
  loading = true;

  constructor(private applicationService: ApplicationService) {}
  //          ↑ Angular injects this automatically

  ngOnInit(): void {
    this.applicationService.getAllApplications().subscribe({
      next: (apps) => {
        this.applications = apps;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
      }
    });
  }
}
```

---

### 5.5 Routing & Guards

Angular's Router maps URLs to components. **Guards** protect routes — essential for TAMM's authenticated service journeys.

```typescript
// src/app/app-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/services',
    pathMatch: 'full'
  },
  {
    path: 'services',
    loadComponent: () => import('./services/service-list/service-list.component')
      .then(m => m.ServiceListComponent)  // Lazy loading — load only when needed
  },
  {
    path: 'services/:serviceId/apply',
    loadComponent: () => import('./journey/journey-wizard/journey-wizard.component')
      .then(m => m.JourneyWizardComponent),
    canActivate: [AuthGuard]   // ← Protected route: requires authentication
  },
  {
    path: 'my-applications',
    loadComponent: () => import('./dashboard/dashboard.component')
      .then(m => m.DashboardComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'my-applications/:id',
    loadComponent: () => import('./dashboard/application-detail/application-detail.component')
      .then(m => m.ApplicationDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./shared/not-found/not-found.component')
      .then(m => m.NotFoundComponent)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'top' })],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

---

### 5.6 Reactive Forms

Reactive Forms are Angular's code-driven approach to forms — powerful validation, dynamic fields, and testability. TAMM uses reactive forms for all service application forms.

```typescript
// src/app/journey/steps/applicant-details/applicant-details.component.ts

import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';

// Custom validator for Emirates ID format
function emiratesIdValidator(control: AbstractControl) {
  const value = control.value as string;
  if (!value) return null;
  // Emirates ID: 784-XXXX-XXXXXXX-X (15 digits without dashes)
  const cleaned = value.replace(/-/g, '');
  return /^\d{15}$/.test(cleaned) ? null : { invalidEmiratesId: true };
}

@Component({
  selector: 'app-applicant-details',
  templateUrl: './applicant-details.component.html'
})
export class ApplicantDetailsComponent implements OnInit {
  @Output() stepComplete = new EventEmitter<Record<string, unknown>>();
  @Output() stepBack = new EventEmitter<void>();

  form!: FormGroup;
  isSubmitting = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      fullName: ['', [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(100)
      ]],
      emiratesId: ['', [
        Validators.required,
        emiratesIdValidator
      ]],
      mobileNumber: ['', [
        Validators.required,
        Validators.pattern(/^\+971[0-9]{9}$/)
      ]],
      email: ['', [
        Validators.required,
        Validators.email
      ]],
      preferredLanguage: ['en', Validators.required]
    });
  }

  // Convenience getter for template access
  get f() { return this.form.controls; }

  getFieldError(field: string): string | null {
    const control = this.form.get(field);
    if (!control || !control.invalid || !control.touched) return null;

    if (control.errors?.['required']) return 'This field is required';
    if (control.errors?.['email']) return 'Enter a valid email address';
    if (control.errors?.['pattern']) return 'Invalid format for UAE mobile';
    if (control.errors?.['invalidEmiratesId']) return 'Emirates ID must be 15 digits';
    if (control.errors?.['minlength']) return `Minimum ${control.errors['minlength'].requiredLength} characters`;
    return 'Invalid value';
  }

  async onSubmit(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();  // Show all errors
      return;
    }
    this.isSubmitting = true;
    this.stepComplete.emit(this.form.value);
    this.isSubmitting = false;
  }
}
```

```html
<!-- applicant-details.component.html -->

<form [formGroup]="form" (ngSubmit)="onSubmit()" novalidate>
  <h2>Applicant Details</h2>

  <!-- Full Name -->
  <div class="form-group" [class.has-error]="f['fullName'].invalid && f['fullName'].touched">
    <label for="fullName">Full Name <span class="required">*</span></label>
    <input
      id="fullName"
      type="text"
      formControlName="fullName"
      placeholder="As per Emirates ID"
    />
    <span class="error-msg" *ngIf="getFieldError('fullName')">
      {{ getFieldError('fullName') }}
    </span>
  </div>

  <!-- Emirates ID -->
  <div class="form-group" [class.has-error]="f['emiratesId'].invalid && f['emiratesId'].touched">
    <label for="emiratesId">Emirates ID <span class="required">*</span></label>
    <input
      id="emiratesId"
      type="text"
      formControlName="emiratesId"
      placeholder="784-XXXX-XXXXXXX-X"
    />
    <span class="error-msg" *ngIf="getFieldError('emiratesId')">
      {{ getFieldError('emiratesId') }}
    </span>
  </div>

  <!-- Mobile -->
  <div class="form-group" [class.has-error]="f['mobileNumber'].invalid && f['mobileNumber'].touched">
    <label for="mobile">Mobile Number <span class="required">*</span></label>
    <input id="mobile" type="tel" formControlName="mobileNumber" placeholder="+971XXXXXXXXX" />
    <span class="error-msg" *ngIf="getFieldError('mobileNumber')">
      {{ getFieldError('mobileNumber') }}
    </span>
  </div>

  <!-- Email -->
  <div class="form-group" [class.has-error]="f['email'].invalid && f['email'].touched">
    <label for="email">Email Address <span class="required">*</span></label>
    <input id="email" type="email" formControlName="email" placeholder="you@example.com" />
    <span class="error-msg" *ngIf="getFieldError('email')">
      {{ getFieldError('email') }}
    </span>
  </div>

  <!-- Actions -->
  <div class="form-actions">
    <button type="button" class="btn-secondary" (click)="stepBack.emit()">← Back</button>
    <button type="submit" class="btn-primary" [disabled]="isSubmitting">
      {{ isSubmitting ? 'Saving...' : 'Continue →' }}
    </button>
  </div>
</form>
```

---

### 5.7 RxJS & Observables

**RxJS** is Angular's reactive programming library. **Observables** are like promises that can emit multiple values over time — essential for TAMM's real-time status updates and form interactivity.

```typescript
// Real-world RxJS usage in a TAMM search component

import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, takeUntil } from 'rxjs/operators';
import { ServiceCatalogueService } from '../core/services/service-catalogue.service';

@Component({
  selector: 'app-service-search',
  template: `
    <input [formControl]="searchControl" placeholder="Search services..." />
    <div *ngFor="let result of searchResults">{{ result.name.en }}</div>
    <div *ngIf="isSearching">Searching...</div>
  `
})
export class ServiceSearchComponent implements OnInit, OnDestroy {
  searchControl = new FormControl('');
  searchResults: any[] = [];
  isSearching = false;

  private destroy$ = new Subject<void>();  // Cleanup signal

  constructor(private catalogueService: ServiceCatalogueService) {}

  ngOnInit(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),           // Wait 300ms after user stops typing
      distinctUntilChanged(),      // Don't search if value didn't change
      switchMap(query => {         // Cancel previous search if user types again
        if (!query || query.length < 2) return [];
        this.isSearching = true;
        return this.catalogueService.search(query);
      }),
      takeUntil(this.destroy$)     // Auto-unsubscribe when component destroys
    ).subscribe({
      next: (results) => {
        this.searchResults = results;
        this.isSearching = false;
      },
      error: () => { this.isSearching = false; }
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();   // Signal cleanup
    this.destroy$.complete();
  }
}
```

> 💡 **The debounceTime + distinctUntilChanged + switchMap pattern** is used across the entire TAMM portal for every search field. Learn it once, use it everywhere.

---

### 5.8 HttpClient

```typescript
// src/app/core/interceptors/auth.interceptor.ts
// Automatically adds the auth token to every HTTP request

import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService, private router: Router) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.authService.getToken();
    const language = localStorage.getItem('tamm_language') || 'en';

    // Clone the request and add headers
    const authReq = req.clone({
      headers: req.headers
        .set('Accept-Language', language)
        .set('X-TAMM-Version', '2.0')
        .set('Authorization', token ? `Bearer ${token}` : '')
    });

    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          this.authService.logout();
          this.router.navigate(['/auth/login']);
        }
        return throwError(() => error);
      })
    );
  }
}
```

---

## 6. TAMM-Specific Patterns in Angular

### 6.1 UAE Pass Auth Guard

```typescript
// src/app/core/guards/auth.guard.ts

import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    if (this.authService.isAuthenticated()) {
      return true;
    }

    // Save intended destination so UAE Pass can redirect back after login
    const intendedUrl = route.pathFromRoot
      .map(r => r.url.map(s => s.path).join('/'))
      .join('/');

    // Redirect to UAE Pass authentication
    this.router.navigate(['/auth/uaepass'], {
      queryParams: { returnUrl: intendedUrl }
    });

    return false;
  }
}
```

---

### 6.2 Bilingual Angular App (ngx-translate)

```bash
npm install @ngx-translate/core @ngx-translate/http-loader
```

```typescript
// src/assets/i18n/en.json
{
  "NAV": {
    "SERVICES": "Services",
    "MY_APPLICATIONS": "My Applications",
    "PROFILE": "My Profile"
  },
  "SERVICE": {
    "APPLY_NOW": "Apply Now",
    "SAVE_DRAFT": "Save Draft",
    "FEE": "Fee",
    "PROCESSING_DAYS": "Processing time"
  },
  "ERRORS": {
    "REQUIRED": "This field is required",
    "EMIRATES_ID": "Emirates ID must be 15 digits"
  }
}
```

```typescript
// src/assets/i18n/ar.json
{
  "NAV": {
    "SERVICES": "الخدمات",
    "MY_APPLICATIONS": "طلباتي",
    "PROFILE": "ملفي الشخصي"
  },
  "SERVICE": {
    "APPLY_NOW": "تقدم الآن",
    "SAVE_DRAFT": "حفظ المسودة",
    "FEE": "الرسوم",
    "PROCESSING_DAYS": "وقت المعالجة"
  },
  "ERRORS": {
    "REQUIRED": "هذا الحقل مطلوب",
    "EMIRATES_ID": "رقم الهوية يجب أن يكون 15 رقماً"
  }
}
```

```html
<!-- Using translations in templates -->
<nav>
  <a routerLink="/services">{{ 'NAV.SERVICES' | translate }}</a>
  <a routerLink="/my-applications">{{ 'NAV.MY_APPLICATIONS' | translate }}</a>
</nav>
<button>{{ 'SERVICE.APPLY_NOW' | translate }}</button>
```

```typescript
// Switching languages programmatically
import { TranslateService } from '@ngx-translate/core';

@Component({ selector: 'app-language-switcher', template: `
  <button (click)="switchLanguage('en')">English</button>
  <button (click)="switchLanguage('ar')">عربي</button>
`})
export class LanguageSwitcherComponent {
  constructor(private translate: TranslateService) {}

  switchLanguage(lang: 'en' | 'ar'): void {
    this.translate.use(lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
    localStorage.setItem('tamm_language', lang);
  }
}
```

---

### 6.3 TAMM Service Form (Reactive Forms)

See Section 5.6 above for the full reactive form implementation. Here is the template binding pattern summary:

```typescript
// Dynamic form fields based on service definition
buildDynamicForm(fields: ServiceField[]): void {
  const group: Record<string, any> = {};
  fields.forEach(field => {
    const validators = [];
    if (field.mandatory) validators.push(Validators.required);
    if (field.type === 'email') validators.push(Validators.email);
    if (field.maxLength) validators.push(Validators.maxLength(field.maxLength));
    group[field.id] = [field.defaultValue || '', validators];
  });
  this.form = this.fb.group(group);
}
```

---

### 6.4 NgRx State for Journey Management

**NgRx** is Angular's Redux implementation using RxJS Observables.

```bash
npm install @ngrx/store @ngrx/effects @ngrx/entity
```

```typescript
// src/app/store/journey/journey.actions.ts

import { createAction, props } from '@ngrx/store';

export const startJourney = createAction(
  '[Journey] Start',
  props<{ serviceId: string; firstStepId: string }>()
);

export const completeStep = createAction(
  '[Journey] Complete Step',
  props<{ stepId: string; data: Record<string, unknown> }>()
);

export const saveDraft = createAction('[Journey] Save Draft');
export const saveDraftSuccess = createAction(
  '[Journey] Save Draft Success',
  props<{ draftId: string }>()
);
export const saveDraftFailure = createAction(
  '[Journey] Save Draft Failure',
  props<{ error: string }>()
);
```

```typescript
// src/app/store/journey/journey.reducer.ts

import { createReducer, on } from '@ngrx/store';
import * as JourneyActions from './journey.actions';

export interface JourneyState {
  serviceId: string | null;
  currentStepId: string | null;
  formData: Record<string, Record<string, unknown>>;
  status: 'idle' | 'in_progress' | 'submitted' | 'failed';
  draftSaving: boolean;
  lastDraftId: string | null;
}

const initialState: JourneyState = {
  serviceId: null,
  currentStepId: null,
  formData: {},
  status: 'idle',
  draftSaving: false,
  lastDraftId: null
};

export const journeyReducer = createReducer(
  initialState,
  on(JourneyActions.startJourney, (state, { serviceId, firstStepId }) => ({
    ...state, serviceId, currentStepId: firstStepId, status: 'in_progress'
  })),
  on(JourneyActions.completeStep, (state, { stepId, data }) => ({
    ...state,
    formData: { ...state.formData, [stepId]: data }
  })),
  on(JourneyActions.saveDraft, state => ({ ...state, draftSaving: true })),
  on(JourneyActions.saveDraftSuccess, (state, { draftId }) => ({
    ...state, draftSaving: false, lastDraftId: draftId
  })),
  on(JourneyActions.saveDraftFailure, state => ({ ...state, draftSaving: false }))
);
```

```typescript
// Using NgRx in a component
import { Store } from '@ngrx/store';
import { completeStep, saveDraft } from '../../store/journey/journey.actions';
import { selectJourneyFormData, selectDraftSaving } from '../../store/journey/journey.selectors';

@Component({ selector: 'app-review', templateUrl: './review.component.html' })
export class ReviewComponent {
  formData$ = this.store.select(selectJourneyFormData);
  draftSaving$ = this.store.select(selectDraftSaving);

  constructor(private store: Store) {}

  saveDraft(): void {
    this.store.dispatch(saveDraft());
  }

  proceed(): void {
    this.store.dispatch(completeStep({ stepId: 'review', data: {} }));
  }
}
```

---

## 7. Step-by-Step: Build a TAMM Portal Page

Let's build a complete Angular TAMM dashboard page that shows a user's applications.

```bash
ng new tamm-portal --routing --style=scss
cd tamm-portal
ng generate service core/services/application
ng generate component dashboard
ng generate component dashboard/application-detail
```

```typescript
// src/app/core/services/application.service.ts — (see Section 5.4 above)
```

```typescript
// src/app/dashboard/dashboard.component.ts

import { Component, OnInit } from '@angular/core';
import { ApplicationService, Application } from '../core/services/application.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  applications: Application[] = [];
  filteredApplications: Application[] = [];
  loading = true;
  error: string | null = null;
  statusFilter = 'all';
  language: 'en' | 'ar' = 'en';

  readonly statusOptions = [
    { value: 'all', label: 'All' },
    { value: 'under_review', label: 'Under Review' },
    { value: 'approved', label: 'Approved' },
    { value: 'documents_required', label: 'Documents Required' }
  ];

  constructor(private applicationService: ApplicationService) {}

  ngOnInit(): void {
    this.applicationService.getAllApplications().subscribe({
      next: (apps) => {
        this.applications = apps;
        this.filteredApplications = apps;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  filterByStatus(status: string): void {
    this.statusFilter = status;
    this.filteredApplications = status === 'all'
      ? this.applications
      : this.applications.filter(a => a.status === status);
  }
}
```

```html
<!-- dashboard.component.html -->

<div class="dashboard" [attr.dir]="language === 'ar' ? 'rtl' : 'ltr'">
  <header class="dash-header">
    <h1>{{ language === 'ar' ? 'طلباتي' : 'My Applications' }}</h1>
    <button class="lang-btn" (click)="language = language === 'en' ? 'ar' : 'en'">
      {{ language === 'en' ? 'عربي' : 'English' }}
    </button>
  </header>

  <!-- Status Filter Tabs -->
  <div class="filter-tabs">
    <button
      *ngFor="let opt of statusOptions"
      [class.active]="statusFilter === opt.value"
      (click)="filterByStatus(opt.value)"
    >
      {{ opt.label }}
    </button>
  </div>

  <!-- Loading -->
  <div *ngIf="loading" class="loading-state">
    <div class="spinner"></div>
    <p>Loading applications...</p>
  </div>

  <!-- Error -->
  <div *ngIf="error" class="error-banner">
    ⚠️ {{ error }}
  </div>

  <!-- Application List -->
  <div *ngIf="!loading && !error" class="application-list">
    <div *ngIf="filteredApplications.length === 0" class="empty-state">
      <p>{{ language === 'ar' ? 'لا توجد طلبات' : 'No applications found' }}</p>
    </div>

    <div
      *ngFor="let app of filteredApplications; trackBy: trackById"
      class="application-card"
      [class]="'status-' + app.status"
      [routerLink]="['/my-applications', app.id]"
    >
      <div class="app-id">{{ app.id }}</div>
      <div class="app-service">{{ app.serviceName }}</div>
      <div class="app-status">
        <span class="status-dot"></span>
        {{ app.status | titlecase | statusLabel }}
      </div>
      <div class="app-date">{{ app.submittedAt | date: 'dd MMM yyyy' }}</div>
      <span class="arrow-icon">›</span>
    </div>
  </div>
</div>
```

```scss
/* dashboard.component.scss */

.dashboard { max-width: 960px; margin: 0 auto; padding: 24px; }
.dash-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.dash-header h1 { font-size: 28px; color: #007DC6; }
.lang-btn { padding: 8px 16px; border: 2px solid #007DC6; border-radius: 20px; color: #007DC6; background: white; cursor: pointer; }

.filter-tabs { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.filter-tabs button { padding: 8px 16px; border: 2px solid #E0E0E0; border-radius: 20px; background: white; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.filter-tabs button.active { background: #007DC6; color: white; border-color: #007DC6; }

.application-card {
  display: grid; grid-template-columns: 140px 1fr 180px 120px 24px;
  align-items: center; gap: 16px;
  padding: 16px 20px; background: white; border-radius: 10px;
  margin-bottom: 12px; box-shadow: 0 1px 6px rgba(0,0,0,0.08);
  cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
  border-inline-start: 4px solid #BDC3C7;
}
.application-card:hover { transform: translateX(4px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.application-card.status-approved { border-inline-start-color: #27AE60; }
.application-card.status-under_review { border-inline-start-color: #F39C12; }
.application-card.status-documents_required { border-inline-start-color: #E74C3C; }

.app-id { font-family: monospace; font-size: 13px; color: #7F8C8D; }
.app-service { font-weight: 600; color: #2C3E50; }
.app-status { display: flex; align-items: center; gap: 6px; font-size: 13px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
.app-date { font-size: 13px; color: #95A5A6; }
.arrow-icon { color: #BDC3C7; font-size: 20px; }

.loading-state { text-align: center; padding: 48px; color: #7F8C8D; }
.error-banner { background: #FDECEC; color: #C0392B; padding: 16px; border-radius: 8px; margin: 16px 0; }
.empty-state { text-align: center; padding: 48px; color: #95A5A6; }
```

---

## 8. Best Practices

```typescript
// ✅ Always unsubscribe from Observables
// Best pattern: use takeUntilDestroyed (Angular 16+)
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

ngOnInit(): void {
  this.service.getData()
    .pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe(data => this.data = data);
}

// ✅ Use the async pipe in templates — unsubscribes automatically
// In component: applications$ = this.applicationService.getAllApplications();
// In template:  <div *ngFor="let app of applications$ | async">

// ✅ Strongly type everything — no `any`
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

// ✅ Use environment files for all configuration
// environments/environment.ts       ← development
// environments/environment.prod.ts  ← production
// Access via: environment.tammApiUrl

// ✅ Lazy load every route — don't load all modules upfront
{
  path: 'journey',
  loadChildren: () => import('./journey/journey.module').then(m => m.JourneyModule)
}

// ✅ TrackBy for ngFor lists — prevents full re-renders
trackById(index: number, item: { id: string }): string {
  return item.id;
}
```

---

## 9. Summary & What's Next

In this module you learned:

- ✅ **What Angular is** — a complete, opinionated TypeScript framework from Google
- ✅ **React vs Angular in TAMM** — Angular for the main portal & admin, React for service micro-frontends
- ✅ **Angular history** — from AngularJS 2010 through the 2016 rewrite to Standalone Components today
- ✅ **Core concepts** — NgModule, Components, Templates, DI, Routing, Guards, Reactive Forms, RxJS, HttpClient
- ✅ **TAMM patterns** — UAE Pass Guard, ngx-translate, dynamic reactive forms, NgRx store
- ✅ **Full Angular dashboard** — bilingual application tracker with filtering

### ➡️ Next: [Module 4 — TAMM Service Lifecycle Deep Dive](./04-service-lifecycle.md)
