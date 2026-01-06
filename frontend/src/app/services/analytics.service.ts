import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

export interface RepoHealth {
    total_commits: number;
    total_merge_requests: number;
    risk_score: number;
}

export interface Correlation {
    jira_key: string;
    commit_sha: string;
    status: string;
}

@Injectable({
    providedIn: 'root'
})
export class AnalyticsService {
    private http = inject(HttpClient);
    private apiUrl = '/api';

    async getRepoHealth(repoId: number): Promise<RepoHealth> {
        return firstValueFrom(this.http.get<RepoHealth>(`${this.apiUrl}/repos/${repoId}/health`));
    }

    async getCorrelations(): Promise<Correlation[]> {
        return firstValueFrom(this.http.get<Correlation[]>(`${this.apiUrl}/analytics/correlations`));
    }

    async getCycleTime(): Promise<any[]> {
        return firstValueFrom(this.http.get<any[]>(`${this.apiUrl}/analytics/cycle-time`));
    }
}
