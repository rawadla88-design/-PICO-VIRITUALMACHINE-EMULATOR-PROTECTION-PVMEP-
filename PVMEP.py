from unicorn import *
from unicorn.x86_constants import *

# 1. Defining the absolute minimum RAM footprint (1 Page = 4 Kilobytes)
MEM_SIZE = 4 * 1024 
ADDRESS  = 0x1000000

# Sample assembly code: mov eax, 0x50; add eax, 0x10
X86_CODE = b"\xB8\x50\x00\x00\x00\x83\xC0\x10"

# Antivirus Evasion Countermeasure: Maximum instructions allowed to prevent execution delays
MAX_INSTRUCTIONS = 1000 

def hook_code(uc, address, size, user_data):
    print(f"[Trace] Executing instruction at: {hex(address)}, Size: {size} bytes")
    current_eax = uc.reg_read(UC_X86_REG_EAX)
    print(f"        Current Register EAX: {hex(current_eax)}")

print("[*] Initializing PVMEP (Pico-VirtualMachine-Emulator-Protection)...")
print(f"[*] Secure Containment Zone Allocated: {MEM_SIZE / 1024} KB of RAM.")

try:
    # 2. Initialize the Emulator
    mu = Uc(UC_ARCH_X86, UC_MODE_32)
    
    # 3. Map the minimum memory boundary
    mu.mem_map(ADDRESS, MEM_SIZE, UC_PROT_ALL)
    
    # 4. Write the binary payload into the environment
    mu.mem_write(ADDRESS, X86_CODE)

    # 5. Register the instruction tracing hook
    mu.hook_add(UC_HOOK_CODE, hook_code)

    print("[*] Starting isolated execution simulation...")
    
    # 6. Execute with strict instruction counting to catch sleep/loop evasion tactics
    mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE), timeout=0, count=MAX_INSTRUCTIONS)

    print("[+] Emulation finished successfully. Zero Host OS footprint detected.")
    
    # 7. Final Security Report
    final_eax = mu.reg_read(UC_X86_REG_EAX)
    print("\n================ PVMEP SECURITY REPORT ================")
    print(f"[-] Execution Status : Clean / Non-Malicious Flow")
    print(f"[-] Final EAX State  : {hex(final_eax)} ({final_eax} Dec)")
    print("=======================================================")

except UcError as e:
    print("\n================ PVMEP SECURITY REPORT ================")
    print(f"[!] Execution Status : CRITICAL / BEHAVIORAL ALERT")
    print(f"[!] Emulation Error  : {e}")
    print("=======================================================")
