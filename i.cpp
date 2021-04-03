#include <bits/stdc++.h>

using namespace std;

bool solve_sub(int n, vector<int> ds, vector<vector<int>> ps, bool switched) {
    auto overtakes = [&](int p0, int p1, int i0_start, int i1_start) {
        // 0, 2, 4, ..., 2(n-1) are sites.
        // 1, 3, ..., 2n-1 are roads in between.
        int i0 = 2 * i0_start;
        int i0_end = (i0 + (2*n-1)) % (2*n);
        int t0 = 0;
        int i1 = 2 * i1_start;
        int t1 = 0;
        int i1_end = (i1 + (2*n-1)) % (2*n);
        bool first = 0;
        while (true)  {
            if (i0 == i0_end || i1 == i1_end) {
                return false;
            }
            if (i0 == i1 && i0 % 2 == 0) {
                return true;
            }
            int remain_0 = (i0 % 2 == 0 ? ps[p0][i0 / 2] : ds[i0 / 2]) - t0;
            int remain_1 = (i1 % 2 == 0 ? ps[p1][i1 / 2] : ds[i1 / 2]) - t1;
            bool move_1 = remain_1 < remain_0;
            if (remain_1 == remain_0) {
                if (i1 % 2 == 0) {
                    move_1 = true;
                } else if (i0 % 2 == 0) {
                    move_1 = false;
                }
                // don't care which one we move here
            }
            if (move_1) {
                t0 += remain_1;
                i1 = (i1 + 1) % (2*n);
                t1 = 0;
            } else {
                t1 += remain_0;
                i0 = (i0 + 1) % (2*n);
                t0 = 0;
            }
            first = false;
        }
    };
    vector<int> xs(3, 0);
    for (int i = 0; i < n; ++i) {
        xs[0] = i;
        for (int j = 0; j < 2; ++j) {
            xs[j + 1] = max(xs[j] + 1, xs[j + 1]);
            // move xs[j+1] so that it is not overtaken by xs[j]
            while (xs[j + 1] + 1 < xs[0] + n && overtakes(j, j + 1, xs[j] % n, xs[j + 1] % n)) {
                ++xs[j + 1];
            }
        }
        bool good = true;
        if (xs[2] >= xs[0] + n) {
            good = false;
        }
        for (int j = 0; j < 3; ++j) {
            if (overtakes(j, (j + 1) % 3, xs[j] % n, xs[(j + 1) % 3] % n)) {
                good = false;
            }
        }
        if (good) {
            if (!switched) {
                cout << xs[0] + 1 << " " << xs[1] + 1 << " " << xs[2] + 1 << "\n";
            } else {
                cout << xs[0] + 1 << " " << xs[2] + 1 << " " << xs[1] + 1 << "\n";
            }
            return true;
        }
    }
    return false;
}

void solve() {
    int n;
    cin >> n;
    vector<int> ds(n);
    for (auto& d : ds) {
        cin >> d;
    }
    vector<vector<int>> ps(3, vector<int>(n));
    for (auto& p : ps) {
        for (auto& x : p) {
            cin >> x;
        }
    }
    if (solve_sub(n, ds, ps, false)) {
        return;
    }
    swap(ps[1], ps[2]);
    if (solve_sub(n, ds, ps, true)) {
        return;
    }
    cout << "impossible\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}