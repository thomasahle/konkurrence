#include <bits/stdc++.h>

using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj_list(n);
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        --u;
        --v;
        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }
    vector<int> state(n, 0);
    vector<int> path;
    int num_moves = 0;
    function<void (int)> dfs = [&](int u) {
        if (state[u] > 0 || num_moves == n) {
            return;
        }
        path.push_back(u);
        state[u] = 1;
        ++num_moves;
        for (int v : adj_list[u]) {
            if (num_moves == n) {
                return;
            }
            dfs(v);
        }
        if (num_moves == n) {
            return;
        }
        path.pop_back();
        state[u] = 2;
        ++num_moves;
    };
    dfs(0);
    cout << path.size() << " " << (n - path.size()) / 2 << "\n";
    for (int p : path) {
        cout << p + 1 << " ";
    }
    cout << "\n";
    for (int u = 0; u < n; ++u) {
        if (state[u] == 0) {
            cout << u + 1 << " ";
        }
    }
    cout << "\n";
    for (int u = 0; u < n; ++u) {
        if (state[u] == 2) {
            cout << u + 1 << " ";
        }
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}