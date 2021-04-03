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
    // i = 0
    us[0] = 0;
    vs[0] = 0;
    case_1.insert({0, 0});
    for (int i = 1; i <= n; ++i) {
        bs[i] = bs[i - 1] + as[i - 1] - 1;
        // beta moves bs[i - 1] to bs[i]
        if (bs[i - 1] < bs[i]) {
            auto it = us.lower_bound(bs[i - 1]);
            while (it != us.end() && it->first < bs[i]) {
                T b = it->first;
                case_1.erase({vs[b], b});
                case_2.insert({it->second, b});
                ++it;
            }
        } else if (bs[i - 1] > bs[i]) {
            // We know that: bs[i] == bs[i - 1] - 1
            T b = bs[i];
            assert (case_2.find({us[b], b}) != case_2.end());
            case_2.erase({us[b], b});
            case_1.insert({vs[b], b});
        }
        for (auto [v, b] : case_1) {
            cerr << "v = " << v << "\n";
            cerr << "b = " << b << "\n";
        }
        for (auto [u, b]: case_2) {
            cerr << "u = " << u << "\n";
            cerr << "b = " << b << "\n";
        }
        ps[i] = max(T(i), bs[i] + i - 1); // special case left hand side
        // for (int j = 0; j < i; ++j) {
        //     // cerr << "ps[i] = " << ps[i] << "\n";
        //     ps[i] = min(ps[i], ps[j] + i - j - 1 + max(bs[i] - bs[j], T(0)) * 2);
        // }
        // cerr << "i = " << i << "\n";
        // cerr << "bs[i] = " << bs[i] << "\n";
        // cerr << "ps[i] = " << ps[i] << "\n";
        if (!case_1.empty()) {
            ps[i] = min(ps[i], case_1.begin()->first + i - 1);
        }
        if (!case_2.empty()) {
            ps[i] = min(ps[i], case_2.begin()->first + 2*bs[i] + i - 1);
        }
        cerr << "i = " << i << "\n";
        cerr << "ps[i] = " << ps[i] << "\n";
        T u_i = ps[i] - i - 2 * bs[i];
        T v_i = ps[i] - i;
        if (us.count(bs[i])) {
            // assert (case_1.find({vs[bs[i]], bs[i]}) != case_1.end());
            // assert (case_2.find({us[bs[i]], bs[i]}) != case_2.end());
            case_1.erase({vs[bs[i]], bs[i]});
            case_2.erase({us[bs[i]], bs[i]});
            us[bs[i]] = min(us[bs[i]], u_i);
            vs[bs[i]] = min(vs[bs[i]], v_i);
        } else {
            us[bs[i]] = u_i;
            us[bs[i]] = v_i;
        }
        if (bs[i] >= bs[i - 1]) {
            case_1.insert({vs[bs[i]], bs[i]});
        } else {
            case_2.insert({us[bs[i]], bs[i]});
        }
    }
    // special case right hand side
    for (int i = 0; i < n; ++i) {
        T S = (bs[n]+n) - (bs[i]+i);
        T L = n - i;
        // cerr << "i = " << i << "\n";
        // cerr << "ps[i] = " << ps[i] << "\n";
        // cerr << "S-1 = " << S-1 << "\n";
        // cerr << "L-1 = " << L-1 << "\n";
        // cerr << "ps[i]+min(S-1,L-1) = " << ps[i]+min(S-1,L-1) << "\n";
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