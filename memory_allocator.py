class MemoryBlock:
    def __init__(self, start, size, is_free=True, process_id=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process_id = process_id

    def __repr__(self):
        status = "Free" if self.is_free else f"Used (P{self.process_id})"
        return f"[{self.start} - {self.start + self.size - 1}] ({status})"


class MemoryAllocator:
    def __init__(self, total_size=1024):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]

    def allocate(self, process_id, size, strategy="first"):
        candidates = [
            (i, block) for i, block in enumerate(self.blocks)
            if block.is_free and block.size >= size
        ]
        if not candidates:
            print(" Allocation failed: No suitable block found.")
            return

        if strategy == "best":
            candidates.sort(key=lambda x: x[1].size)
        elif strategy == "worst":
            candidates.sort(key=lambda x: x[1].size, reverse=True)
        # else: first-fit (default)

        index, block = candidates[0]

        if block.size > size:
            new_block = MemoryBlock(block.start + size, block.size - size)
            self.blocks.insert(index + 1, new_block)

        block.size = size
        block.is_free = False
        block.process_id = process_id
        print(f" Process P{process_id} allocated at address {block.start}")

    def free(self, process_id):
        for i, block in enumerate(self.blocks):
            if not block.is_free and block.process_id == process_id:
                block.is_free = True
                block.process_id = None
                print(f" Process P{process_id} deallocated.")

                # Merge with next
                if i + 1 < len(self.blocks) and self.blocks[i + 1].is_free:
                    block.size += self.blocks[i + 1].size
                    del self.blocks[i + 1]
                # Merge with previous
                if i - 1 >= 0 and self.blocks[i - 1].is_free:
                    self.blocks[i - 1].size += block.size
                    del self.blocks[i]
                return
        print(f" Process P{process_id} not found.")

    def compact(self):
        print(" Compacting memory...")
        new_blocks = []
        current_address = 0
        for block in self.blocks:
            if not block.is_free:
                new_blocks.append(MemoryBlock(current_address, block.size, False, block.process_id))
                current_address += block.size
        free_size = self.total_size - current_address
        if free_size > 0:
            new_blocks.append(MemoryBlock(current_address, free_size))
        self.blocks = new_blocks
        print(" Compaction complete.")

    def display(self):
        print("\n Memory Blocks:")
        for block in self.blocks:
            print(block)


# === Terminal UI ===

def main():
    allocator = MemoryAllocator()

    while True:
        print("\n Choose an operation:")
        print("1 - Allocate process")
        print("2 - Free process")
        print("3 - Display memory")
        print("4 - Compact memory")
        print("5 - Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            try:
                pid = int(input("Enter process ID: "))
                size = int(input(" Enter process size: "))
                strategy = input(" Enter allocation strategy (first/best/worst): ").lower()
                if strategy not in ("first", "best", "worst"):
                    print(" Invalid strategy. Try again.")
                    continue
                allocator.allocate(pid, size, strategy)
            except ValueError:
                print(" Invalid input. Please enter numbers for ID and size.")

        elif choice == "2":
            try:
                pid = int(input(" Enter process ID to free: "))
                allocator.free(pid)
            except ValueError:
                print(" Invalid input.")

        elif choice == "3":
            allocator.display()

        elif choice == "4":
            allocator.compact()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print(" Invalid choice. Try again.")


if __name__ == "__main__":
    main()
