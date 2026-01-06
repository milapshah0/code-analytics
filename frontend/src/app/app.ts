import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { AnalyticsService, Correlation, RepoHealth } from './services/analytics.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class AppComponent implements OnInit {
  analyticsService = inject(AnalyticsService);

  repoHealth = signal<RepoHealth | null>(null);
  correlations = signal<Correlation[]>([]);
  cycleTime = signal<any[]>([]);

  async ngOnInit() {
    try {
      // For demo purposes, we'll try to fetch repo health for ID 1
      this.repoHealth.set(await this.analyticsService.getRepoHealth(1));
      this.correlations.set(await this.analyticsService.getCorrelations());
      this.cycleTime.set(await this.analyticsService.getCycleTime());
    } catch (e) {
      console.error('Failed to fetch initial data', e);
    }
  }
}
