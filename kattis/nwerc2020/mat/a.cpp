#include <bits/stdc++.h>

using namespace std;

template<typename T>
void solve() {
    int n, q;
    cin >> n >> q;
    vector<T> xs(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> xs[i];
    }
    int M = 200 * n;
    vector<T> best(M, 0);
    for (int i = 1; i <= n; ++i) {
        best[i] = xs[i];
    }
    for (int i = n + 1; i < M; ++i) {
        best[i] = best[i - 1] + xs[1];
        for (int j = 2; j <= n; ++j) {
            best[i] = min(best[i], best[i - j] + xs[j]);
        }
    }
    int best_per = 1;
    for (int i = 1; i <= n; ++i) {
        // if (best[i] / i <= best[best_per] / best_per) {
        if (best[i] * best_per <= best[best_per] * i) {
            best_per = i;
        }
    }
    while (q --> 0) {
        int x;
        cin >> x;
        if (x < M) {
            cout << best[x] << "\n";
        } else {
            int t = (x - M - 1) / best_per + 2;
            cout << best[x - t * best_per] + t * best[best_per] << "\n";
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve<long long>();
    return 0;
}