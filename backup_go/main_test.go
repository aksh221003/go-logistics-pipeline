package main
import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("The math is wrong! Expected 5 but got %d", result)
    }
}