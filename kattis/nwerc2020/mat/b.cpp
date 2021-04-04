#include <bits/stdc++.h>

using namespace std;

template<typename T>
void solve() {
    int n;
    cin >> n;
    vector<T> as(n);
    for (auto& a : as) {
        cin >> a;
    }
    vector<T> bs(n + 1, 0);
    vector<T> ps(n + 1, 0);
    map<T, T> us, vs;
    set<pair<T, T>> case_1, case_2;
    set<T> b1s, b2s;
    T beta;
    auto add_b = [&](T b, T u, T v) {
        if (us.count(b)) {
            if (b >= beta) {
                case_1.erase({vs[b], b});
            } else {
                case_2.erase({us[b], b});
            }
            us[b] = min(us[b], u);
            vs[b] = min(vs[b], v);
        } else {
            us[b] = u;
            vs[b] = v;
        }
        if (b >= beta) {
            case_1.insert({vs[b], b});
            b1s.insert(b);
        } else {
            case_2.insert({us[b], b});
            b2s.insert(b);
        }
    };
    auto set_beta = [&](T new_beta) {
        beta = new_beta;
        while (!b1s.empty()) {
            T b = *b1s.begin();
            if (b >= beta) {
                break;
            }
            b1s.erase(b);
            case_1.erase({vs[b], b});
            case_2.insert({us[b], b});
            b2s.insert(b);
        }
        while (!b2s.empty()) {
            T b = *b2s.rbegin();
            if (b < beta) {
                break;
            }
            b2s.erase(b);
            case_2.erase({us[b], b});
            case_1.insert({vs[b], b});
            b1s.insert(b);
        }
    };
    // i = 0
    add_b(0, 0, 0);
    for (int i = 1; i <= n; ++i) {
        bs[i] = bs[i - 1] + as[i - 1] - 1;
        // beta moves bs[i - 1] to bs[i]
        set_beta(bs[i]);
        ps[i] = max(T(i), bs[i] + i - 1); // special case left hand side
        if (!case_1.empty()) {
            ps[i] = min(ps[i], case_1.begin()->first + i - 1);
        }
        if (!case_2.empty()) {
            ps[i] = min(ps[i], case_2.begin()->first + 2*bs[i] + i - 1);
        }
        T u_i = ps[i] - i - 2 * bs[i];
        T v_i = ps[i] - i;
        add_b(bs[i], u_i, v_i);
    }
    // special case right hand side
    for (int i = 0; i < n; ++i) {
        T S = (bs[n]+n) - (bs[i]+i);
        T L = n - i;
        ps[n] = min(ps[n], ps[i] + max(S-1, L-1));
    }
    cout << ps[n] << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve<long long>();
    return 0;
}