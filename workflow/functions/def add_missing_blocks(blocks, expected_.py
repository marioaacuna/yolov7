def add_missing_blocks(blocks, expected_gap=900, max_gap=1200):
    blocks.sort(key=lambda x: x['Block_Start'])  # Sort blocks by start frame
    updated_blocks = []

    for i in range(len(blocks)):
        current_block = blocks[i]
        current_block['Artificially_added'] = 0  # Original blocks are not artificially added
        updated_blocks.append(current_block)

        # If this is the last block or the next block has a different label, skip
        if i == len(blocks) - 1 or blocks[i+1]['Label'] != current_block['Label']:
            continue

        # Check the gap to the next block
        next_block = blocks[i+1]
        gap_to_next_block = next_block['Block_Start'] - current_block['Block_End']

        # If there's a large gap to the next block, and it's not the start of a new group
        if gap_to_next_block > max_gap and (i == 0 or blocks[i-1]['Label'] != current_block['Label'] or current_block['Block_Start'] - blocks[i-1]['Block_End'] > max_gap):
            # Add an artificial block
            artificial_block_start = current_block['Block_End'] + expected_gap
            artificial_block = {
                'Label': current_block['Label'],
                'Block_Start': artificial_block_start,
                'Block_End': artificial_block_start,
                'Withdrawal_Frame': artificial_block_start - 1,
                'Artificially_added': 1
            }
            updated_blocks.append(artificial_block)

    # Sort the blocks again in case artificial blocks were added
    updated_blocks.sort(key=lambda x: x['Block_Start'])
    return updated_blocks

# Example usage (blocks should be your original list of blocks):
updated_blocks = add_missing_blocks(filtered_results)
