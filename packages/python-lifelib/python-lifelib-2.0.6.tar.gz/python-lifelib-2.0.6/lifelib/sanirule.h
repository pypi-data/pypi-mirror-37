#include <string>
#include <stdint.h>

namespace apg {

    bool replace(std::string& str, const std::string& from, const std::string& to) {
        size_t start_pos = str.find(from);
        if (start_pos == std::string::npos)
            return false;
        str.replace(start_pos, from.length(), to);
        return true;
    }

    std::string gollyrule(std::string inrule) {
        std::string outrule = inrule;

        if (outrule[0] == 'g') {
            size_t i = 1;
            while ((i < outrule.length()) && ('0' <= outrule[i]) && (outrule[i] <= '9')) {
                i += 1;
            }
            outrule = outrule.substr(i) + "/" + outrule.substr(1, i-1);
        }

        if (outrule[0] == 'b') {
            replace(outrule,"b","B");
            replace(outrule,"s","/S");
        } else if (outrule[0] == 'r') {
            replace(outrule,"b",",");
            replace(outrule,"t",",");
            replace(outrule,"s",",");
            replace(outrule,"t",",");
            outrule = outrule.substr(1);
        }
        return outrule;
    }

    std::string sanirule(std::string inrule) {

        std::string outrule = inrule;
        int slashcount = 0;

        while (outrule.length() > 0) {
            char x = outrule[outrule.length() - 1];
            if ((x == ' ') || (x == '\n') || (x == '\r') || (x == '\t')) {
                outrule = outrule.substr(0, outrule.length() - 1);
            } else {
                break;
            }
        }

        while (outrule.length() > 0) {
            char x = outrule[0];
            if ((x == ' ') || (x == '=')) {
                outrule = outrule.substr(1);
            } else {
                break;
            }
        }

        for (uint32_t i = 0; i < outrule.length(); i++) {
            slashcount += (outrule[i] == '/');
        }

        if ((slashcount >= 1) && (outrule[0] != 'B')) {
            size_t slash_pos = outrule.find("/");
            if (slash_pos != std::string::npos) {
                std::string first_part = outrule.substr(0, slash_pos);
                std::string second_part = outrule.substr(slash_pos + 1);
                slash_pos = second_part.find("/");
                if (slash_pos != std::string::npos) {
                    outrule = "B" + second_part.substr(0, slash_pos) + "/S" + first_part + second_part.substr(slash_pos);
                } else {
                    outrule = "B" + second_part + "/S" + first_part;
                }
            }
        }

        if (slashcount >= 1) {
            replace(outrule, "B", "b");
            replace(outrule, "/S", "s");
            size_t slash_pos = outrule.find("/");
            if (slash_pos != std::string::npos) {
                outrule = "g" + outrule.substr(slash_pos + 1) + outrule.substr(0, slash_pos);
            }
        }

        replace(outrule, "PedestrianLife", "b38s23");
        replace(outrule, "DryLife", "b37s23");
        replace(outrule, "HighLife", "b36s23");
        replace(outrule, "Life", "b3s23");
        return outrule;
    }
}
