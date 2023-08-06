
    template<int H, int K = 2>
    struct VTile {

        uint64_t coords; // 8 bytes

        uint32_t hash; // 4 bytes
        int16_t population; // 2 bytes
        uint8_t updateflags; // 1 byte
        uint8_t currentflags; // 1 byte

        VTile<H,K> *neighbours[6]; // 48 bytes
        uint32_t d[H + 2*K]; // 128 bytes
        uint32_t hist[H + 2*K]; // 128 bytes

        constexpr static uint32_t middle = ((1u << (32 - K)) - (1u << K)); // e.g. 0x3ffffffcu

        bool nonempty(uint64_t z) {
            uint32_t* q = z ? hist : d;
            for (int i = K; i < H + K; i++) {
                if (q[i] & middle) { return true; }
            }
            return false;
        }

        void clearHistory() {
            std::memset(hist, 0, 4 * (H+2*K));
        }

        void copyBoundary12(VTile<H,K> *n1, VTile<H,K> *n2) __attribute__((always_inline)) {
            for (int i = 0; i < K; i++) {
                d[i] = ((n1->d[H+i] << 14) & 0xffff0000u) | ((n2->d[H+i] >> 14) & 0x0000ffffu);
            }
        }

        void copyBoundary1(VTile<H,K> *n) __attribute__((always_inline)) {
            for (int i = 0; i < K; i++) {
                d[i] = ((n->d[H+i] << 14) & 0xffff0000u) | (d[i] & 0x0000ffffu);
            }
        }

        void copyBoundary2(VTile<H,K> *n) __attribute__((always_inline)) {
            for (int i = 0; i < K; i++) {
                d[i] = ((n->d[H+i] >> 14) & 0x0000ffffu) | (d[i] & 0xffff0000u);
            }
        }

        void copyBoundary45(VTile<H,K> *n4, VTile<H,K> *n5) __attribute__((always_inline)) {
            for (int i = K; i < 2*K; i++) {
                d[H+i] = ((n5->d[i] << 14) & 0xffff0000u) | ((n4->d[i] >> 14) & 0x0000ffffu);
            }
        }

        void copyBoundary4(VTile<H,K> *n) __attribute__((always_inline)) {
            for (int i = K; i < 2*K; i++) {
                d[H+i] = ((n->d[i] >> 14) & 0x0000ffffu) | (d[H+i] & 0xffff0000u);
            }
        }

        void copyBoundary5(VTile<H,K> *n) __attribute__((always_inline)) {
            for (int i = K; i < 2*K; i++) {
                d[H+i] = ((n->d[i] << 14) & 0xffff0000u) | (d[H+i] & 0x0000ffffu);
            }
        }

        // These functions depend on hand-written assembly which differs
        // depending on the values of H and K. We therefore need to define
        // the functions later, and merely declare them here:
        void copyBoundary3(VTile<H,K> *n);
        void copyBoundary0(VTile<H,K> *n);
        inline void updateTile(upattern<VTile<H,K>, 32 - 2*K, H>* owner, int rule, int family, int mantissa) __attribute__((always_inline));
        // ^^^ we really do need both the prefix 'inline' and the attribute 'always_inline' for this to work ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        uint32_t hashTile() {
            if (currentflags & 2) { return hash; }
            uint32_t partialhash = 0;

            for (int i = K; i < H + K; i++) {
                partialhash = partialhash * (partialhash + 77232917) + i * (d[i] & middle);
            }

            hash = partialhash;
            currentflags |= 2;
            return partialhash;
        }

        inline static int countpop64(const uint64_t *y) __attribute__((always_inline)) {

            int pop = 0;

            constexpr uint64_t middlemiddle = ((uint64_t) middle) * 0x100000001ull;

            // We include two popcounts in the loop so that the number of
            // iterations is halved (in the case of H = 44, from 22 to 11).
            // This knocks it below the threshold such that gcc will unroll
            // the loop (completely).
            for (int i = 0; i < H / 2; i += 2) {
                pop += __builtin_popcountll(y[i] & middlemiddle);
                pop += __builtin_popcountll(y[i+1] & middlemiddle);
            }

            return pop;

        }

        int countPopulation() {

            // Check memoized value:
            if (currentflags & 1) { return population; }

            // Casting to 64-bit values so we can halve the number of calls
            // to the POPCNT instruction. If H = 44, for example, we only
            // need to perform 22 copies of the instruction.
            population = countpop64((uint64_t *) (d + K));
            currentflags |= 1;
            return population;
        }

        bitworld to_bitworld(int z) {
            uint32_t* q = (z ? hist : d);
            bitworld bw;
            uint32_t e[H + 2*K] = {0};
            for (uint64_t i = 0; i < H; i++) {
                e[i] = (q[i + K] & middle) >> K;
            }
            uint64_t f[4];
            for (uint64_t j = 0; j < ((H + 2*K) / 8); j++) {
                int bis = best_instruction_set();
                if (bis >= 9) {
                    twofifths_avx(e + (8*j), f);
                } else {
                    twofifths_sse2(e + (8*j), f);
                }
                for (uint64_t i = 0; i < 4; i++) {
                    if (f[i]) { bw.world.emplace(std::pair<int32_t, int32_t>(i, j), f[i]); }
                }
            }
            return bw;
        }

        void eu64(upattern<VTile<H,K>, 32 - 2*K, H>* owner, int z, uint8_t dx, uint8_t dy, uint64_t v) {

            if ((v == 0) || (z >= 2)) { return; }

            for (int i = 0; i < 6; i++) { owner->updateNeighbour(this, i); }
            if (updateflags == 0) { owner->modified.push_back(this); }
            updateflags |= 64;

            uint32_t* q = (z ? hist : d);

            if (dy > H - 8) {
                owner->getNeighbour(this, 4)->eu64(owner, z, dx + (16 - K), 0, v >> (8 * (H - dy)));
            }
            if (dx >= (32 - 2*K)) {
                owner->getNeighbour(this, 0)->eu64(owner, z, dx - (32 - 2*K), dy, v);
            } else if (dx > (24 - 2*K)) {
                uint64_t bitmask = 0x0101010101010101ull;
                bitmask = (bitmask << (dx - (24 - 2*K))) - bitmask;
                owner->getNeighbour(this, 0)->eu64(owner, z, 0, dy, (v >> ((32 - 2*K) - dx)) & bitmask);
            }

            if (dx < (32 - 2*K)) {
                for (uint64_t i = 0; i < 8; i++) {
                    uint64_t newy = i + dy;
                    if (newy < H) {
                        q[newy + K] |= ((((v >> (8 * i)) & 255) << (dx + K)) & middle);
                    }
                }
            }
        }

    };
