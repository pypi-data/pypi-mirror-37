
# This file defines the genera accepted by lifelib. Earlier genera take
# precedence over later genera, so (for example) the rule b38s23 belongs
# to the genus 'lifelike' rather than 'isotropic'.

genus_list = []
genus_list.append({'name': 'b3s23life', 'regex': 'b3s23'})
genus_list.append({'name': 'lifelike', 'regex': 'b0?1?2?3?4?5?6?7?8?s0?1?2?3?4?5?6?7?8?'})
genus_list.append({'name': 'generations', 'regex': 'g[1-9][0-9]*b1?2?3?4?5?6?7?8?s0?1?2?3?4?5?6?7?8?'})
genus_list.append({'name': 'isotropic', 'regex': 'b[1-9ceaiknjqrytwz-]*s[0-9ceaiknjqrytwz-]*'})
genus_list.append({'name': 'ltl', 'regex': 'r[234567]b[1-9][0-9]*t[1-9][0-9]*s[1-9][0-9]*t[1-9][0-9]*'})
genus_list.append({'name': 'gltl', 'regex': 'g[1-9][0-9]*r[234567]b[1-9][0-9]*t[1-9][0-9]*s[1-9][0-9]*t[1-9][0-9]*'})
genus_list.append({'name': 'isogeny', 'regex': 'g[1-9][0-9]*b[1-9ceaiknjqrytwz-]*s[0-9ceaiknjqrytwz-]*'})
genus_list.append({'name': 'bsfkl', 'regex': 'b1?2?3?4?5?6?7?8?s0?1?2?3?4?5?6?7?8?f0?1?2?3?4?5?6?7?8?k0?1?2?3?4?5?6?7?8?l0?1?2?3?4?5?6?7?8?'})
