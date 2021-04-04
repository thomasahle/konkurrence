#include <bits/stdc++.h>

using namespace std;

void solve() {
    int n, r, m;
    cin >> n >> r >> m;
    vector<int> ts(m);
    vector<double> probs(m);
    vector<double> penalty(m);
    for (int i = 0; i < m; ++i) {
        cin >> ts[i] >> probs[i] >> penalty[i];
    }
    m += 1;
    ts.push_back(n);
    probs.push_back(1);
    penalty.push_back(0);
    vector<int> good(m), bad(m);
    for (int i = 0; i < m; ++i) {
        good[i] = i > 0 ? ts[i] - ts[i - 1] : ts[i];
        bad[i] = good[i] + penalty[i];
    }
    auto f = [&](double x) {
        vector<vector<double>> res(m + 1, vector<double>(r, x));
        for (int j = 0; j < r; ++j) {
            res[m][j] = 0;
        }
        for (int i = m - 1; i >= 0; --i) {
            for (int j = 0; j < r; ++j) {
                double good_case = (j + good[i] < r ? res[i + 1][j + good[i]] : x);
                double bad_case = j + bad[i] < r ? res[i + 1][j + bad[i]] + bad[i] - good[i] : x;
                bad_case = min(bad_case, x);
                res[i][j] = good[i] + probs[i] * good_case + (1 - probs[i]) * bad_case;
            }
        }
        return res[0][0];
    };
    double lo = n, hi = ((double) 50000) * r;
    for (int i = 0; i < 200; ++i) {
        double mid = (hi + lo) / 2;
        // cerr << "mid = " << mid << "\n";
        // cerr << "f(mid) = " << f(mid) << "\n";
        if (f(mid) > mid) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    cout << setprecision(20) << lo << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}