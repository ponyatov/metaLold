package io.github.ponyatov.metal;

public class Frame {

    /// type/class tag
    String type;

    /// object value (primitive implementation language type)
    String value;

    /// construct new frame/object with given name
    public Frame(String V) {
        type  = "frame";
        value = V;
    }

    /// dump in short form: header only
    public String head() {
        return "<" + type + ":" + value + ">";
    }

}
