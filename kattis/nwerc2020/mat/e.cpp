#include <bits/stdc++.h>

using namespace std;

struct com {
    int x, y;
    com() {}
    com(int x, int y): x(x), y(y) {}
    com operator+(const com& o) const {
        return com(x+o.x, y+o.y);
    }
    com operator-(const com& o) const {
        return com(x-o.x, y-o.y);
    }
    bool operator==(const com& o) const {
        return make_pair(x, y) == make_pair(o.x, o.y);
    }
    bool operator!=(const com& o) const {
        return make_pair(x, y) != make_pair(o.x, o.y);
    }
    bool operator<(const com& o) const {
        return make_pair(x, y) < make_pair(o.x, o.y);
    }
};

void solve() {
    int n;
    cin >> n;
    vector<com> ms(n);
    com a, b;
    {
        int ax, ay;
        cin >> ax >> ay;
        a = {ax, ay};
    }
    {
        int bx, by;
        cin >> bx >> by;
        b = {bx, by};
    }
    for (auto& m : ms) {
        int x, y;
        cin >> x >> y;
        m = {x, y};
    }
    auto is_valid = [&](com c) {
        return 1 <= c.x && c.x <= n && 1 <= c.y && c.y <= n;
    };
    auto moves_to = [&](com x) {
        set<com> s;
        for (auto& m : ms) {
            if (is_valid(x - m)) {
                s.insert(x - m);
            }
        }
        return s;
    };
    auto moves_from = [&](com x) {
        set<com> s;
        for (auto& m : ms) {
            if (is_valid(x + m)) {
                s.insert(x + m);
            }
        }
        return s;
    };
    auto can_reach = [&](com x, com y) {
        set<com> s1 = moves_from(x);
        set<com> s2 = moves_to(y);
        if (s1.count(y)) {
            return true;
        }
        for (com z : s1) {
            if (s2.count(z)) {
                return true;
            }
        }
        return false;
    };
    if (can_reach(a, b)) {
        cout << "Alice wins\n";
        return;
    }
    bool bob_wins = n <= 20;
    if (bob_wins) {
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= n; ++j) {
                com z = {i, j};
                if (z != b && !can_reach(b, z)) {
                    bob_wins = false;
                }
            }
        }
    }
    if (bob_wins) {
        cout << "Bob wins\n";
        return;
    }
    // mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    mt19937 rng(43121223);
    while (true) {
        com z = com(rng() % n + 1, rng() % n + 1);
        if (z != b && !can_reach(b, z)) {
            cout << "tie " << z.x << " " << z.y << "\n";
            break;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}