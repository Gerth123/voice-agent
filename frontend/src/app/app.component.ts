import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <main class="shell">
      <section class="panel">
        <p class="eyebrow">Voice Agent MVP</p>
        <h1>Admin UI</h1>
        <p>
          The Angular frontend is ready for settings, calls, calendar connections,
          and provider configuration.
        </p>
      </section>
    </main>
  `,
  styles: [
    `
      .shell {
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 32px;
      }

      .panel {
        width: min(720px, 100%);
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 8px;
        padding: 32px;
        box-shadow: 0 12px 32px rgb(29 36 51 / 8%);
      }

      .eyebrow {
        margin: 0 0 8px;
        color: #526071;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
      }

      h1 {
        margin: 0 0 16px;
        font-size: 32px;
      }

      p {
        margin: 0;
        line-height: 1.6;
      }
    `
  ]
})
export class AppComponent {}

