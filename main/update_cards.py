import add_card
import crawler

def updateCards(deckname):
    lcards = add_card.Request('findNotes', query=f'deck:{deckname}')._result
    succeeded = []
    failed = []
    totalsize = len(lcards)
    count = 0
    for cardid in lcards:
        count += 1
        print(f'{count}/{totalsize}')

        # find the word
        result = add_card.Request('notesInfo', notes=[cardid])._result[0]
        if result['modelName'] == 'anki_auto-lookup':
            word = result['fields']['word']['value']
        elif result['modelName'] == 'Basic':
            word = result['fields']['English words']['value']
        else:
            raise Exception('UnknownModel')

        print(f'{word}: started')

        # lookup
        lurequest = crawler.LookupRequest(word)
        lurequest.onlineLookup()
        entry = lurequest.export()

        if entry != None:

            # get fields
            fields = add_card.add_note(entry, export=True)

            # update
            add_card.Request('updateNoteFields', note={'id': cardid, 'fields': fields}) 
            add_card.Request('updateNoteFields', note={'id': cardid, 'fields': fields}) 


            print(f'{word}: updated')
            succeeded.append((cardid, word))

        else:
            print(f'{word}: update failed')
            failed.append((cardid, word))

    print('writing log...')

    with open('succeeded.txt', 'w') as f:
        for word in succeeded:
            f.write(f'{word[0]} {word[1]}\n')

    with open('failed.txt', 'w') as f:
        for word in failed:
            f.write(f'{word[0]} {word[1]}\n')

    print('done')

if __name__ == "__main__":
    updateCards('Vocabulary')
