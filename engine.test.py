def test(irs_engine):
    print('===Running Tests===')

    epsilon = 1e-4

    print("Cosine Similarity Test")
    queries = prob.split(", ")
    for i, query in enumerate(queries):
        num_total += 1
        ranked = irsys.query_rank(query)
        top_rank = ranked[0]
        if top_rank[0] == soln[i][0]:
            if top_rank[1] >= float(soln[i][1]) - epsilon and \
                    top_rank[1] <= float(soln[i][1]) + epsilon:
                num_correct += 1

    feedback = "%d/%d Correct. Accuracy: %f" % \
            (num_correct, num_total, float(num_correct)/num_total)

    points = num_correct * 25 /num_total
    print( "    Score: %d Feedback: %s" % (points, feedback))
