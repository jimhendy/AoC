#include <iostream>
#include <fstream> // Include this header for file stream classes
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <deque>
#include <string>
#include <algorithm>

using namespace std;

// Define the Point2D class
class Point2D
{
public:
    int x, y;

    Point2D(int x = 0, int y = 0) : x(x), y(y) {}

    bool operator==(const Point2D &other) const
    {
        return x == other.x && y == other.y;
    }

    Point2D operator+(const Point2D &other) const
    {
        return Point2D(x + other.x, y + other.y);
    }

    std::vector<Point2D> nb4() const
    {
        return {
            Point2D(x + 1, y),
            Point2D(x - 1, y),
            Point2D(x, y + 1),
            Point2D(x, y - 1)};
    }

    struct HashFunction
    {
        size_t operator()(const Point2D &point) const
        {
            return std::hash<int>()(point.x) ^ std::hash<int>()(point.y);
        }
    };
};

Point2D DESTINATION;
std::unordered_map<Point2D, std::unordered_map<Point2D, int, Point2D::HashFunction>, Point2D::HashFunction> CONNECTIONS;

class State
{
public:
    Point2D position;
    std::unordered_set<Point2D, Point2D::HashFunction> history;
    int steps;

    State(Point2D position, std::unordered_set<Point2D, Point2D::HashFunction> history, int steps = 0)
        : position(position), history(history), steps(steps) {}

    bool is_complete() const
    {
        return position == DESTINATION;
    }

    std::vector<State> all_possible_next_states() const
    {
        std::unordered_set<Point2D, Point2D::HashFunction> new_history = history;
        new_history.insert(position);

        std::vector<State> next_states;
        const auto &connections = CONNECTIONS.at(position);
        for (const auto &[next_location, extra_steps] : connections)
        {
            if (new_history.find(next_location) == new_history.end())
            {
                next_states.emplace_back(next_location, new_history, steps + extra_steps);
            }
        }
        return next_states;
    }
};

int run(const std::string &inputs)
{
    Point2D start;
    bool start_set = false;
    std::unordered_set<Point2D, Point2D::HashFunction> all_spaces;
    std::vector<std::string> lines;
    size_t pos = 0, end;

    // Split input into lines
    while ((end = inputs.find('\n', pos)) != std::string::npos)
    {
        lines.push_back(inputs.substr(pos, end - pos));
        pos = end + 1;
    }
    lines.push_back(inputs.substr(pos));

    for (int y = 0; y < lines.size(); ++y)
    {
        const std::string &line = lines[y];
        for (int x = 0; x < line.length(); ++x)
        {
            Point2D point(x, y);
            if (line[x] == '.')
            {
                if (!start_set)
                {
                    start = point;
                    start_set = true;
                }
                DESTINATION = point;
            }
            if (line[x] != '#')
            {
                all_spaces.insert(point);
            }
        }
    }

    // Log out the start and destination
    std::cout << "Start: " << start.x << ", " << start.y << std::endl;
    std::cout << "Destination: " << DESTINATION.x << ", " << DESTINATION.y << std::endl;

    // Construct connections
    for (const auto &point : all_spaces)
    {
        auto &connections = CONNECTIONS[point];
        for (const auto &next_point : point.nb4())
        {
            if (all_spaces.find(next_point) != all_spaces.end())
            {
                connections[next_point] = 1;
            }
        }
    }

    // Simplify connections
    for (const auto &point : all_spaces)
    {
        auto &connected_points = CONNECTIONS[point];
        if (connected_points.size() == 2)
        {
            auto it = connected_points.begin();
            Point2D a = it->first;
            int steps_to_a = it->second;
            ++it;
            Point2D b = it->first;
            int steps_to_b = it->second;

            CONNECTIONS[a][b] = steps_to_a + steps_to_b;
            CONNECTIONS[b][a] = steps_to_a + steps_to_b;

            CONNECTIONS[a].erase(point);
            CONNECTIONS[b].erase(point);
            CONNECTIONS.erase(point);
        }
    }

    // BFS to find the longest path
    std::deque<State> queue;
    queue.emplace_back(start, std::unordered_set<Point2D, Point2D::HashFunction>());
    std::vector<State> complete;

    while (!queue.empty())
    {
        State state = queue.front();
        queue.pop_front();
        if (state.is_complete())
        {
            complete.push_back(state);
        }
        else
        {
            for (const auto &next_state : state.all_possible_next_states())
            {
                queue.push_back(next_state);
            }
        }
    }

    int max_steps = 0;
    for (const auto &state : complete)
    {
        if (state.steps > max_steps)
        {
            max_steps = state.steps;
        }
    }
    return max_steps;
}

int main()
{
    std::ifstream file("input.txt");
    if (!file.is_open())
    {
        std::cerr << "Unable to open file input.txt" << std::endl;
        return 1;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string inputs = buffer.str();
    int result = run(inputs);
    std::cout << result << std::endl;

    return result;
}
